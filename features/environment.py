import json
import logging
import time
import uuid
from datetime import datetime

import requests

from config import Config
from utilties.rabbit_context import RabbitContext


def before_all(_):
    logging.getLogger('pika').setLevel('ERROR')
    logging.getLogger('paramiko').setLevel('ERROR')
    logging.captureWarnings(True)


def before_scenario(context, _):
    context.test_start_local_datetime = datetime.now()
    context.action_plan_id = str(uuid.uuid4())
    _clear_down_all_queues()


def get_msg_count(queue_name):
    uri = f'http://{Config.RABBITMQ_HOST}:{Config.RABBITMQ_MAN_PORT}/api/queues/%2f/{queue_name}'
    response = requests.get(uri, auth=(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))
    response.raise_for_status()
    response_data = json.loads(response.content)

    return response_data['messages']


def _clear_down_all_queues():
    all_queues = _get_all_queues()

    for queue in all_queues:
        # keep killing this Delayed queue, just to stop it redlivering anything in some mad race condition
        _clear_down_queue(Config.RABBITMQ_DELAYED_REDELIVERY_QUEUE)
        _clear_down_queue(queue)


def _get_all_queues():
    uri = f'http://{Config.RABBITMQ_HOST}:{Config.RABBITMQ_MAN_PORT}/api/queues/%2f/'
    response = requests.get(uri, auth=(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))
    response.raise_for_status()
    response_data = json.loads(response.content)

    return [queue['name'] for queue in response_data]


def _clear_down_queue(queue_name):
    failed_attempts = 0

    while True:
        uri = f'http://{Config.RABBITMQ_HOST}:{Config.RABBITMQ_MAN_PORT}/api/queues/%2f/{queue_name}/contents'
        response = requests.delete(uri, auth=(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))

        if response.status_code != 200 and response.status_code != 204:
            # When clearing down very large queues, e.g. millions of rows on rh.case.uac it can timeout, so retry
            failed_attempts = failed_attempts + 1

            if failed_attempts >= 10:
                response.raise_for_status()

            print(f'Failed with {response.status_code} retry attempt {failed_attempts}')
            time.sleep(10)

        if get_msg_count(queue_name) == 0:
            return

        time.sleep(1)


def add_test_queue(binding_key, exchange_name, queue_name, exchange_type='topic'):
    with RabbitContext() as rabbit:
        rabbit.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)
        rabbit.channel.queue_declare(queue=queue_name, durable=True)
        rabbit.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)
