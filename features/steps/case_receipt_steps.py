import functools
import json
import time
from datetime import datetime

from behave import step

from config import Config
from utilties.rabbit_context import RabbitContext
from utilties.rabbit_helper import wait_for_queue_to_be_drained, start_listening_to_rabbit_queue, \
    store_all_msgs_in_context


@step("we gather a list of QIDs")
def gather_qids(context):
    context.messages_received = []
    start_listening_to_rabbit_queue(Config.RABBITMQ_RH_OUTBOUND_UAC_QUEUE, functools.partial(
        store_all_msgs_in_context, context=context,
        expected_msg_count=context.message_count,
        type_filter='UAC_UPDATED'))


@step("case processor receipts at an acceptable rate")
def case_processor_receipt_test(context):
    json_receipt_messages = [_create_receipt_msg(message['payload']['uac']['questionnaireId']) for message in
                             context.messages_received]

    test_start_time = datetime.utcnow()
    with RabbitContext(queue_name=Config.CASE_RECEIPT_QUEUE_NAME) as rabbit:
        for receipt_message in json_receipt_messages:
            rabbit.publish_message(
                message=receipt_message,
                content_type='application/json')

    time.sleep(10)
    wait_for_queue_to_be_drained(Config.CASE_RECEIPT_QUEUE_NAME)

    test_complete_time = datetime.utcnow() - test_start_time

    time_taken_metric = json.dumps({
        'event_description': f'Time for case processor to receipt {str(len(json_receipt_messages))} messages',
        'event_type': 'CASE_PROCESSOR_RECEIPT_PERFORMANCE',
        'time_in_seconds': str(test_complete_time.total_seconds()),
        'time_taken': str(test_complete_time)
    })
    print(f'{time_taken_metric}\n')


def _create_receipt_msg(qid):
    json_message = json.dumps({
        "event": {
            "type": "RESPONSE_RECEIVED",
            "source": "RECEIPT_SERVICE",
            "channel": "EQ",
            "dateTime": "2011-08-12T20:17:46.384Z",
            "transactionId": "3a5c8f53-c729-44c1-b890-0fba6ab26a27"
        },
        "payload": {
            "response": {
                "questionnaireId": qid,
            }
        }
    })
    return json_message
