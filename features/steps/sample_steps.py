from datetime import datetime
from pathlib import Path
from time import sleep

from behave import step
from load_sample import load_sample_file

from config import Config


@step('the sample file has been loaded')
def loading_sample(context):
    sample_file_name = Path(Config.SAMPLE_FILE)
    context.sample_load_time = datetime.utcnow()
    load_sample_file(sample_file_name, context.action_plan_id,
                     context.action_plan_id,
                     host=Config.RABBITMQ_HOST, port=Config.RABBITMQ_PORT,
                     vhost=Config.RABBITMQ_VHOST, exchange=Config.RABBITMQ_EXCHANGE,
                     user=Config.RABBITMQ_USER, password=Config.RABBITMQ_PASSWORD,
                     queue_name=Config.RABBITMQ_SAMPLE_INBOUND_QUEUE)


@step("the action rules trigger")
def wait_for_sample_ingestion(_context):
    sleep(Config.DELAY_FOR_ACTION_RULE_AND_SAMPLE_LOAD * 60)

