from pathlib import Path
from time import sleep

from behave import step
from load_sample import load_sample_file

from config import Config


@step('the sample file has been loaded')
def loading_sample(context):
    sample_file_name = Path('/resources/sample_files/sample_file')

    load_sample_file(sample_file_name, context.collection_exercise_id,
                     context.action_plan_id,
                     host=Config.RABBITMQ_HOST, port=Config.RABBITMQ_PORT,
                     vhost=Config.RABBITMQ_VHOST, exchange=Config.RABBITMQ_EXCHANGE,
                     user=Config.RABBITMQ_USER, password=Config.RABBITMQ_PASSWORD,
                     queue_name=Config.RABBITMQ_SAMPLE_INBOUND_QUEUE)


@step('an time has passed to allow for full sample ingestion')
def wait_for_sample_ingestion():
    sleep(Config.SAMPLE_SLEEP*60)
