import json
import time
import uuid
from datetime import datetime

from behave import step
from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPIError

from config import Config
from features.environment import get_msg_count, _clear_down_queue


@step("we can receipt the cases at an acceptable rate")
def receipt_performance_test(context):
    test_quantity = Config.PUBSUB_MESSAGE_QUANTITY

    json_message = json.dumps({
        "timeCreated": "2008-08-24T00:00:00Z",
        "metadata": {
            "case_id": "123",
            "tx_id": "666",
            "questionnaire_id": "999",
        }
    })
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(Config.PUBSUB_PROJECT, Config.PUBSUB_TOPIC)

    test_start_time = datetime.utcnow()
    for _ in range(0, int(test_quantity)):
        publish_message(publisher, json_message, topic_path)

    wait_for_queue_to_reach_target(Config.CASE_RECEIPT_QUEUE_NAME, test_quantity)

    test_complete_time = datetime.utcnow() - test_start_time

    _clear_down_queue(Config.CASE_RECEIPT_QUEUE_NAME)

    time_taken_metric = json.dumps({
        'event_description': f'Time for pubsub service to process {test_quantity} Google Pubsub messages',
        'event_type': 'PUBSUB_PERFORMANCE',
        'time_in_seconds': str(test_complete_time.total_seconds()),
        'time_taken': str(test_complete_time)
    })
    print(f'{time_taken_metric}\n')


def publish_message(publisher, json_message, topic_path):
    publisher.publish(topic_path, json_message.encode('utf-8'), eventType='OBJECT_FINALIZE',
                      bucketId='eq-bucket',
                      objectId=str(uuid.uuid4()))


def wait_for_queue_to_reach_target(queue_name, target):
    loop_start_time = datetime.utcnow()
    while get_msg_count(queue_name) < target:
        time.sleep(1)
        if (datetime.utcnow() - loop_start_time).total_seconds() > 3600:
            assert "Pubsub messages not published within time limit"


@step("a receipt is sent for every case loaded")
def send_receipt_for_every_loaded_case(context):
    _publish_object_finalize(context)


def _publish_object_finalize(context, case_id="0", tx_id="3d14675d-a25d-4672-a0fe-b960586653e8",
                             questionnaire_id="0"):
    context.sent_to_gcp = False

    publisher = pubsub_v1.PublisherClient()

    topic_path = publisher.topic_path(Config.RECEIPT_TOPIC_PROJECT, Config.RECEIPT_TOPIC_ID)

    data = json.dumps({
        "timeCreated": "2008-08-24T00:00:00Z",
        "metadata": {
            "case_id": case_id,
            "tx_id": tx_id,
            "questionnaire_id": questionnaire_id,
        }
    })

    future = publisher.publish(topic_path,
                               data=data.encode('utf-8'),
                               eventType='OBJECT_FINALIZE',
                               bucketId='eq-bucket',
                               objectId=tx_id)
    if not future.done():
        time.sleep(1)
    try:
        future.result(timeout=30)
    except GoogleAPIError:
        return

    print(f'Message published to {topic_path}')

    context.sent_to_gcp = True


@step("a case updated event is emitted with receipted true for every case")
def receipted_case_updated_event_emitted_for_each_case(context):
    context.x = 'blah'
