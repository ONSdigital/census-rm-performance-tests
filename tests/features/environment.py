import base64
import json
import uuid
from datetime import datetime

from config import Config
from tests.utilties.rabbit_context import RabbitContext


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
        rabbit.channel.queue_purge(queue=Config.RABBITMQ_OUTBOUND_FIELD_QUEUE_TEST)
        rabbit.channel.queue_purge(queue=Config.RABBITMQ_UNADDRESSED_REQUEST_QUEUE)


def _setup_google_auth():
    if Config.GOOGLE_SERVICE_ACCOUNT_JSON and Config.GOOGLE_APPLICATION_CREDENTIALS:
        sa_json = json.loads(base64.b64decode(Config.GOOGLE_SERVICE_ACCOUNT_JSON))
        with open(Config.GOOGLE_APPLICATION_CREDENTIALS, 'w') as credentials_file:
            json.dump(sa_json, credentials_file)
        print(f'Created GOOGLE_APPLICATION_CREDENTIALS: {Config.GOOGLE_APPLICATION_CREDENTIALS}')
