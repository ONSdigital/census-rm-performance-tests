import datetime
import json
import time
import uuid

from behave import step
from google.cloud import pubsub_v1

from config import Config
from features.environment import get_msg_count


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
    for _ in range(0, test_quantity):
        publish_message(publisher, json_message, topic_path)

    wait_for_queue_to_reach_target(Config.CASE_RECEIPT_QUEUE_NAME, test_quantity)

    test_complete_time = datetime.utcnow() - test_start_time

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
