import time
from datetime import datetime
from pathlib import Path

from behave import step
from load_sample import load_sample_file

from config import Config
from features.environment import get_msg_count


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

    # Not ideal but seems to not work sometimes otherwise, shouldn't have time ramifications though
    time.sleep(10)
    _wait_for_queue_to_be_drained(Config.RABBITMQ_SAMPLE_INBOUND_QUEUE)
    _wait_for_queue_to_be_drained(Config.RABBITMQ_SAMPLE_TO_ACTION_QUEUE)


def _wait_for_queue_to_be_drained(queue_name):
    while True:
        if get_msg_count(queue_name) == 0:
            return

        time.sleep(1)
