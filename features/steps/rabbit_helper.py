import functools
import json
import logging

from structlog import wrap_logger

from utilties.rabbit_context import RabbitContext

logger = wrap_logger(logging.getLogger(__name__))


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
    assert False, "Didn't find the expected number of messages"


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


def store_first_message_in_context(ch, method, _properties, body, context, type_filter=None):
    parsed_body = json.loads(body)
    if parsed_body['event']['type'] == type_filter or type_filter is None:
        context.first_message = parsed_body
        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.stop_consuming()
    else:
        ch.basic_nack(delivery_tag=method.delivery_tag)


def add_test_queue(binding_key, exchange_name, queue_name, exchange_type='topic'):
    with RabbitContext() as rabbit:
        rabbit.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)
        rabbit.channel.queue_declare(queue=queue_name, durable=True)
        rabbit.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)
        logger.info('Successfully add test queue to rabbitmq', exchange=exchange_name, binding=binding_key)


def purge_queues(*queues):
    with RabbitContext() as rabbit:
        for queue in queues:
            rabbit.channel.queue_purge(queue=queue)


def check_no_msgs_sent_to_queue(queue, on_message_callback, timeout=5):
    rabbit = RabbitContext(queue_name=queue)
    connection = rabbit.open_connection()

    connection.call_later(
        delay=timeout,
        callback=functools.partial(_timeout_callback_expected, rabbit))

    rabbit.channel.basic_consume(
        queue=queue,
        on_message_callback=on_message_callback)
    rabbit.channel.start_consuming()


def _timeout_callback_expected(rabbit):
    rabbit.close_connection()
