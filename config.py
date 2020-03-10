import os
from pathlib import Path


class Config:
    PROJECT_PATH = Path(__file__).parent
    PROTOCOL = os.getenv('PROTOCOL', 'http')

    ACTION_SERVICE_HOST = os.getenv('ACTION_SERVICE_HOST', 'localhost')
    ACTION_SERVICE_PORT = os.getenv('ACTION_SERVICE_PORT', '8301')
    ACTION_SERVICE = f'{PROTOCOL}://{ACTION_SERVICE_HOST}:{ACTION_SERVICE_PORT}'

    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST', 'localhost')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT', '6672')
    RABBITMQ_MAN_PORT = os.getenv('RABBITMQ_MAN_PORT', '16672')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    RABBITMQ_SAMPLE_INBOUND_QUEUE = os.getenv('RABBITMQ_QUEUE', 'case.sample.inbound')
    RABBITMQ_SAMPLE_TO_ACTION_QUEUE = 'case.action'
    RABBITMQ_RH_OUTBOUND_CASE_QUEUE = os.getenv('RABBITMQ_RH_OUTBOUND_CASE_QUEUE', 'case.rh.case')
    RABBITMQ_RH_OUTBOUND_UAC_QUEUE = os.getenv('RABBITMQ_RH_OUTBOUND_UAC_QUEUE', 'case.rh.uac')
    RABBITMQ_UNADDRESSED_REQUEST_QUEUE = os.getenv('RABBITMQ_UNADDRESSED_REQUEST_QUEUE', 'unaddressedRequestQueue')
    RABBITMQ_OUTBOUND_FIELD_QUEUE = os.getenv('RABBITMQ_OUTBOUND_FIELD_QUEUE', 'Action.Field')
    RABBITMQ_INBOUND_EQ_QUEUE = os.getenv('RABBITMQ_INBOUND_EQ_QUEUE', 'Case.Responses')
    RABBITMQ_DELAYED_REDELIVERY_QUEUE = 'delayedRedeliveryQueue'
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')

    SFTP_HOST = os.getenv('SFTP_HOST', 'localhost')
    SFTP_PORT = os.getenv('SFTP_PORT', '122')
    SFTP_USERNAME = os.getenv('SFTP_USERNAME', 'centos')
    SFTP_SSH_KEY_PATH = Path(os.getenv('SFTP_SSH_KEY_PATH',
                                       PROJECT_PATH.joinpath('resources', 'dummy_keys', 'dummy_sftp_private_key')))
    SFTP_PASSPHRASE = os.getenv('SFTP_PASSPHRASE', 'secret')
    SFTP_PPO_DIRECTORY = os.getenv('SFTP_PPO_DIRECTORY', 'ppo_dev/print_services/')
    SFTP_QM_DIRECTORY = os.getenv('SFTP_QM_DIRECTORY', 'qmprint_dev/print_services/')
    SFTP_POLLING_DELAY_SECONDS = os.getenv('SFTP_POLLING_DELAY_SECONDS', 1)

    DECRYPTION_KEY_PATH = Path(os.getenv('DECRYPTION_KEY_PATH',
                                         PROJECT_PATH.joinpath('resources', 'dummy_keys', 'our_dummy_private.asc')))
    DECRYPTION_KEY_PASSPHRASE = os.getenv('DECRYPTION_KEY_PATH', 'test')

    SAMPLE_FILE_PATH = Path(os.getenv('SAMPLE_FILE_PATH', PROJECT_PATH.joinpath('resources', 'sample_files',
                                                                                '100_per_treatment_code.csv')))

    SAMPLE_BUCKET = os.getenv('SAMPLE_BUCKET', 'census-rm-performance-sample-files')

    CASE_RECEIPT_SAMPLE_FILE = Path(os.getenv('SAMPLE_FILE_PATH', PROJECT_PATH.joinpath('resources', 'sample_files',
                                                                                        '10000_sample_file.csv')))

    PUBSUB_MESSAGE_QUANTITY = 5000
    CASE_RECEIPT_QUEUE_NAME = "Case.Responses"
    PUBSUB_PROJECT = os.getenv('PUBSUB_PROJECT', "census-rm-performance")
    PUBSUB_TOPIC = os.getenv('PUBSUB_TOPIC', "receipting-topic-performance")

    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
