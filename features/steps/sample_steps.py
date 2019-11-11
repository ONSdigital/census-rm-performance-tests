import json
import time
from datetime import datetime
from pathlib import Path

import requests
from behave import step
from load_sample import load_sample_file

from config import Config


@step("the sample file has been loaded fully into the action db")
def loading_sample(context):
    sample_file_name = Path(Config.SAMPLE_FILE_PATH)

    context.sample_load_time = datetime.utcnow()
    load_sample_file(sample_file_name, context.action_plan_id,
                     context.action_plan_id,
                     host=Config.RABBITMQ_HOST, port=Config.RABBITMQ_PORT,
                     vhost=Config.RABBITMQ_VHOST, exchange=Config.RABBITMQ_EXCHANGE,
                     user=Config.RABBITMQ_USER, password=Config.RABBITMQ_PASSWORD,
                     queue_name=Config.RABBITMQ_SAMPLE_INBOUND_QUEUE)

    # 1st check that the case.sample.inbound queue is empty, if it works try removing some of these here sleeps
    time.sleep(10)
    _check_queue_is_empty("case.sample.inbound")
    print("case.sample.inbound Is empty")
    time.sleep(10)
    _check_queue_is_empty("case.action")
    print("case.action is empty")

    time.sleep(10)


def _check_queue_is_empty(queue_name):
    while True:
        uri = f'http://{Config.RABBITMQ_HOST}:{Config.RABBITMQ_MAN_PORT}/api/queues/%2f/{queue_name}'
        response = requests.get(uri, auth=(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))
        response.raise_for_status()

        response_data = json.loads(response.content)

        if response_data['messages'] == 0:
            return

        time.sleep(2)
