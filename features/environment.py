import logging
import uuid
from datetime import datetime

from config import Config
from utilties.rabbit_context import RabbitContext


def before_all(_):
    logging.getLogger('pika').setLevel('ERROR')
    logging.getLogger('paramiko').setLevel('ERROR')
    logging.captureWarnings(True)


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
        rabbit.channel.queue_purge(queue=Config.RABBITMQ_UNADDRESSED_REQUEST_QUEUE)


def add_test_queue(binding_key, exchange_name, queue_name, exchange_type='topic'):
    with RabbitContext() as rabbit:
        rabbit.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)
        rabbit.channel.queue_declare(queue=queue_name, durable=True)
        rabbit.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)
