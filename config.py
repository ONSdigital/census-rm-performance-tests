import os
from pathlib import Path


class Config:
    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME', 'admin')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD', 'secret')
    BASIC_AUTH = (SECURITY_USER_NAME, SECURITY_USER_PASSWORD)

    PROTOCOL = os.getenv('PROTOCOL', 'http')

    ACTION_SERVICE_HOST = os.getenv('ACTION_SERVICE_HOST', 'localhost')
    ACTION_SERVICE_PORT = os.getenv('ACTION_SERVICE_PORT', '8301')
    ACTION_SERVICE = f'{PROTOCOL}://{ACTION_SERVICE_HOST}:{ACTION_SERVICE_PORT}'

    CASEAPI_SERVICE_HOST = os.getenv('CASEAPI_SERVICE_HOST', 'localhost')
    CASEAPI_SERVICE_PORT = os.getenv('CASEAPI_SERVICE_PORT', '8161')
    CASEAPI_SERVICE = f'{PROTOCOL}://{CASEAPI_SERVICE_HOST}:{CASEAPI_SERVICE_PORT}'

    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST', 'localhost')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT', '6672')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    RABBITMQ_SAMPLE_INBOUND_QUEUE = os.getenv('RABBITMQ_QUEUE', 'case.sample.inbound')
    RABBITMQ_RH_OUTBOUND_CASE_QUEUE = os.getenv('RABBITMQ_RH_OUTBOUND_CASE_QUEUE', 'case.rh.case')
    RABBITMQ_RH_OUTBOUND_UAC_QUEUE = os.getenv('RABBITMQ_RH_OUTBOUND_UAC_QUEUE', 'case.rh.uac')
    RABBITMQ_UNADDRESSED_REQUEST_QUEUE = os.getenv('RABBITMQ_UNADDRESSED_REQUEST_QUEUE', 'unaddressedRequestQueue')
    RABBITMQ_OUTBOUND_FIELD_QUEUE = os.getenv('RABBITMQ_OUTBOUND_FIELD_QUEUE', 'Action.Field')
    RABBITMQ_INBOUND_EQ_QUEUE = os.getenv('RABBITMQ_INBOUND_EQ_QUEUE', 'Case.Responses')
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')

    SFTP_HOST = os.getenv('SFTP_HOST', 'localhost')
    SFTP_PORT = os.getenv('SFTP_PORT', '122')
    SFTP_USERNAME = os.getenv('SFTP_USERNAME', 'centos')
    SFTP_KEY_FILENAME = os.getenv('SFTP_KEY_FILENAME', 'dummy_sftp_private_key')
    SFTP_KEY = os.getenv('SFTP_KEY', None)
    SFTP_PASSPHRASE = os.getenv('SFTP_PASSPHRASE', 'secret')
    SFTP_PPO_DIRECTORY = os.getenv('SFTP_PPO_DIRECTORY', 'ppo_dev/print_services/')
    SFTP_QM_DIRECTORY = os.getenv('SFTP_QM_DIRECTORY', 'qmprint_dev/print_services/')
    SFTP_POLLING_DELAY = os.getenv('SFTP_POLLING_DELAY', 1)

    RECEIPT_TOPIC_PROJECT = os.getenv('RECEIPT_TOPIC_PROJECT', 'project')
    RECEIPT_TOPIC_ID = os.getenv('RECEIPT_TOPIC_ID', 'eq-submission-topic')

    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')

    # For test queues
    RABBITMQ_RH_OUTBOUND_CASE_QUEUE_TEST = 'case.rh.case.test'
    RABBITMQ_CASE_TEST_ROUTE = os.getenv('RH_CASE_ROUTING_KEY', 'event.case.*')
    RABBITMQ_RH_OUTBOUND_UAC_QUEUE_TEST = 'case.rh.uac.test'
    RABBITMQ_UAC_TEST_ROUTE = os.getenv('RH_UAC_ROUTING_KEY', "event.uac.*")
    RABBITMQ_RH_EXCHANGE_NAME = os.getenv('RH_EXCHANGE_NAME', "events")
    RABBITMQ_OUTBOUND_FIELD_QUEUE_TEST = 'Action.Field.Test'
    RABBITMQ_FIELD_TEST_ROUTE = os.getenv('FWMT_ROUTING_KEY', 'Action.Field.binding')
    RABBITMQ_FIELD_EXCHNAGE_NAME = os.getenv('FWMT_EXCHANGE_NAME', 'action-outbound-exchange')

    DELAY_FOR_ACTION_RULE_AND_SAMPLE_LOAD = os.getenv('DELAY_FOR_ACTION_RULE_AND_SAMPLE_LOAD', 0.5)
    SAMPLE_FILE = os.getenv('SAMPLE_FILE', Path('resources/sample_files/sample_file.csv'))

    P_CI_H1_EXPECTED = os.getenv('P_CI_H1_EXPECTED', 9)
    P_CI_H2_EXPECTED = os.getenv('P_CI_H2_EXPECTED', 9)
    P_CI_H4_EXPECTED = os.getenv('P_CI_H4_EXPECTED', 1)

    P_CI_ICL1_EXPECTED = os.getenv('P_CI_ICL1_EXPECTED', 12)
    P_CI_ICL2B_EXPECTED = os.getenv('P_CI_ICL2B_EXPECTED', 12)
    P_CI_ICL4_EXPECTED = os.getenv('P_CI_ICL4_EXPECTED', 2)

