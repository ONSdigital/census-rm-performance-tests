import json
import time
from google.cloud import storage
from datetime import datetime
from pathlib import Path

from behave import step
from load_sample import load_sample_file

from config import Config
from utilties.rabbit_helper import wait_for_queue_to_be_drained, wait_for_messages_to_be_queued


@step("the sample file has been loaded from the bucket")
def load_bucket_sample_file(context):
    client = storage.Client()

    bucket = client.get_bucket(Config.SAMPLE_BUCKET)
    blob = storage.Blob(Config.THREE_MILLION_SAMPLE_FILE, bucket)

    context.sample_file = 'sample_file_from_bucket.csv'

    with open(context.sample_file, 'wb+') as file_obj:
        client.download_blob_to_file(blob, file_obj)

    print(f'downloaded file {Config.THREE_MILLION_SAMPLE_FILE} from gcp bucket {Config.SAMPLE_BUCKET}, now loading')

    load_file(context, Path(context.sample_file))


@step("the sample file has been loaded")
def load_sample(context):
    context.sample_file = Config.SAMPLE_FILE_PATH
    load_file(context, Path(Config.SAMPLE_FILE_PATH))


def load_file(context, sample_file_name):
    context.sample_load_start_time = datetime.utcnow()

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
    wait_for_queue_to_be_drained(Config.RABBITMQ_SAMPLE_INBOUND_QUEUE)
    wait_for_queue_to_be_drained(Config.RABBITMQ_SAMPLE_TO_ACTION_QUEUE)
    context.sample_fully_ingested_time = datetime.utcnow()
    time_taken = context.sample_fully_ingested_time - context.sample_load_start_time
    time_taken_metric = json.dumps({
        'event_description': 'Time to fully ingest sample into action scheduler',
        'event_type': 'SAMPLE_INGEST_TO_ACTION_CASES',
        'time_in_seconds': str(time_taken.total_seconds()),
        'time_taken': str(time_taken)
    })
    print(f'{time_taken_metric}\n')


@step("the sample file '{sample_file}' is loaded and '{message_count}' messages are queued on '{queue}'")
def load_sample_and_check_queue(context, sample_file, message_count, queue):
    context.message_count = int(message_count)
    load_file(context, Config.PROJECT_PATH.joinpath('resources', 'sample_files', sample_file))
    wait_for_messages_to_be_queued(queue, context.message_count)
