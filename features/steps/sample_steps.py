import time
from google.cloud import storage
from datetime import datetime
from pathlib import Path

from behave import step
from load_sample import load_sample_file

from config import Config
from features.environment import get_msg_count


@step('the sample file {sample_file} has been loaded from the bucket {bucket}')
def load_bucket_sample_file(context, sample_file, bucket):
    client = storage.Client()

    bucket = client.get_bucket(bucket)
    blob = storage.Blob(sample_file, bucket)

    context.sample_file = 'sample_file_from_bucket.csv'

    with open(context.sample_file, 'wb+') as file_obj:
        client.download_blob_to_file(blob, file_obj)

    print('downloaded file from gcp bucket, attempting loading now')

    load_file(context, Path(context.sample_file))


@step("the sample file has been loaded")
def load_sample(context):
    context.sample_file = Config.SAMPLE_FILE_PATH
    load_file(context, Path(Config.SAMPLE_FILE_PATH))


def load_file(context, sample_file_name):
    context.sample_load_start_time = datetime.utcnow()

    print('Sample file name: ', sample_file_name)

    load_sample_file(sample_file_name, context.action_plan_id,
                     context.action_plan_id,
                     host=Config.RABBITMQ_HOST, port=Config.RABBITMQ_PORT,
                     vhost=Config.RABBITMQ_VHOST, exchange=Config.RABBITMQ_EXCHANGE,
                     user=Config.RABBITMQ_USER, password=Config.RABBITMQ_PASSWORD,
                     queue_name=Config.RABBITMQ_SAMPLE_INBOUND_QUEUE)


@step("the sample has been fully ingested into action scheduler database")
def wait_for_full_sample_ingest(context):
    # Wait required to consistently work
    time.sleep(10)
    _wait_for_queue_to_be_drained(Config.RABBITMQ_SAMPLE_INBOUND_QUEUE)
    _wait_for_queue_to_be_drained(Config.RABBITMQ_SAMPLE_TO_ACTION_QUEUE)
    context.sample_fully_ingested_time = datetime.utcnow()
    print(f'Time to fully ingest sample into action scheduler: '
          f'[{str(context.sample_fully_ingested_time - context.sample_load_start_time)}]\n')


def _wait_for_queue_to_be_drained(queue_name):
    while True:
        if get_msg_count(queue_name) == 0:
            return

        time.sleep(1)
