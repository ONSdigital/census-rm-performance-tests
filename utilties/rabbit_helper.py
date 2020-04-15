import functools
import json
import logging
import time

from structlog import wrap_logger

from features.environment import get_msg_count
from utilties.rabbit_context import RabbitContext

logger = wrap_logger(logging.getLogger(__name__))


def wait_for_queue_to_be_drained(queue_name):
    attempts = 0
    logger.info(f"Waiting for queue '{queue_name}' to be drained")
    while get_msg_count(queue_name) != 0:
        time.sleep(1)
        attempts += 1
        if not attempts % 200:
            logger.info(f"Still waiting for queue '{queue_name}' to be drained")
    logger.info(f"Queue '{queue_name}' has been drained")


def wait_for_messages_to_be_queued(queue_name, message_count):
    while get_msg_count(queue_name) < message_count:
        time.sleep(1)


def start_listening_to_rabbit_queue(queue, on_message_callback, timeout=30):
    rabbit = RabbitContext(queue_name=queue)
    connection = rabbit.open_connection()

    connection.call_later(
        delay=timeout,
        callback=functools.partial(_timeout_callback, rabbit))

    rabbit.channel.basic_consume(
        queue=queue,
        on_message_callback=on_message_callback)
    rabbit.channel.start_consuming()


def _timeout_callback(rabbit):
    logger.error('Timed out waiting for messages')
    rabbit.close_connection()


def store_all_msgs_in_context(ch, method, _properties, body, context, expected_msg_count, type_filter=None):
    parsed_body = json.loads(body)

    if parsed_body['event']['type'] == type_filter or type_filter is None:
        context.messages_received.append(parsed_body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        # take it, ignore it?
        ch.basic_nack(delivery_tag=method.delivery_tag)

    if len(context.messages_received) == expected_msg_count:
        ch.stop_consuming()
