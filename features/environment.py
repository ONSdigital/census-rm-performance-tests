import uuid
from datetime import datetime

from config import Config
from utilties.rabbit_context import RabbitContext


def before_all(_):

    add_test_queue(Config.RABBITMQ_CASE_TEST_ROUTE, Config.RABBITMQ_RH_EXCHANGE_NAME,
                   Config.RABBITMQ_RH_OUTBOUND_CASE_QUEUE_TEST)
    add_test_queue(Config.RABBITMQ_UAC_TEST_ROUTE, Config.RABBITMQ_RH_EXCHANGE_NAME,
                   Config.RABBITMQ_RH_OUTBOUND_UAC_QUEUE_TEST)
    add_test_queue(Config.RABBITMQ_FIELD_TEST_ROUTE, Config.RABBITMQ_FIELD_EXCHNAGE_NAME,
                   Config.RABBITMQ_OUTBOUND_FIELD_QUEUE_TEST, 'direct')


def before_scenario(context, _):
    context.test_start_local_datetime = datetime.now()
    context.action_plan_id = str(uuid.uuid4())
    _purge_queues()


def _purge_queues():
    with RabbitContext() as rabbit:
        rabbit.channel.queue_purge(queue=Config.RABBITMQ_RH_OUTBOUND_CASE_QUEUE)
        rabbit.channel.queue_purge(queue=Config.RABBITMQ_RH_OUTBOUND_UAC_QUEUE)
        rabbit.channel.queue_purge(queue=Config.RABBITMQ_SAMPLE_INBOUND_QUEUE)
        rabbit.channel.queue_purge(queue=Config.RABBITMQ_OUTBOUND_FIELD_QUEUE)
        rabbit.channel.queue_purge(queue=Config.RABBITMQ_RH_OUTBOUND_CASE_QUEUE_TEST)
        rabbit.channel.queue_purge(queue=Config.RABBITMQ_RH_OUTBOUND_UAC_QUEUE_TEST)
        rabbit.channel.queue_purge(queue=Config.RABBITMQ_UNADDRESSED_REQUEST_QUEUE)


def add_test_queue(binding_key, exchange_name, queue_name, exchange_type='topic'):
    with RabbitContext() as rabbit:
        rabbit.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)
        rabbit.channel.queue_declare(queue=queue_name, durable=True)
        rabbit.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)
