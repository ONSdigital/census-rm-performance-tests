import logging
from datetime import datetime
from pathlib import Path
from time import sleep

import paramiko
import pgpy
from behave import step
from structlog import wrap_logger

from config import Config
from utilties.mappings import PACK_CODE_TO_SFTP_DIRECTORY, PRINT_FILES_EXPECTED
from utilties.sftp_utility import SftpUtility

logger = wrap_logger(logging.getLogger(__name__))


# timeout in concourse to stop it going on forever
@step('all the initial contact print files are produced on the SFTP')
def wait_for_print_files(context):
    with SftpUtility() as sftp:
        while True:
            context.all_initial_print_sftp_paths = fetch_all_print_files_paths(sftp)
            if context.all_initial_print_sftp_paths:
                context.produced_print_file_time = datetime.utcnow()
                break
            sleep(int(Config.SFTP_POLLING_DELAY))


def fetch_all_print_files_paths(sftp):
    print_file_paths = []
    print_file_paths.extend([f'{Config.SFTP_QM_DIRECTORY}{str(file_name.filename)}' for file_name in
                             sftp.get_all_print_files_paths(Config.SFTP_QM_DIRECTORY)])
    print_file_paths.extend([f'{Config.SFTP_QM_DIRECTORY}{str(file_name.filename)}' for file_name in
                             sftp.get_all_print_files_paths(Config.SFTP_PPO_DIRECTORY)])

    for packcode in PACK_CODE_TO_SFTP_DIRECTORY.keys():
        matching_csv_files = [print_file_path for print_file_path in print_file_paths
                              if packcode in print_file_path and print_file_path.endswith('.csv.gpg')]
        matching_manifest_files = [
            print_file_path for print_file_path in print_file_paths
            if print_file_path.startswith(packcode) and print_file_path.endswith('.manifest')]
        if len(matching_csv_files) != 1 and len(matching_manifest_files) != 1:
            return []
    return print_file_paths


@step('they all have the correct line count')
def print_file_line_count(context):
    initial_contact_csv_paths = [path for path in context.all_initial_print_sftp_paths
                                 if path.endswith('.csv')]
    print_dict = {'print_files': dict(list())}
    sftp = open_sftp_client()
    for initial_contact_path in initial_contact_csv_paths:
        with sftp.open(initial_contact_path) as initial_contact_print_file:
            decrypted_print_file = decrypt_message(initial_contact_print_file.read(), Path(__file__).parents[2]
                                                   .joinpath('resources', 'dummy_keys', 'our_dummy_private.asc'),
                                                   'test')
        print_dict['print_files'][Path(initial_contact_path)] = decrypted_print_file

    for print_file_path, print_file_message in print_dict['print_files'].items():
        packcode = '_'.join(print_file_path.name.split('_')[0:3])
        assert PRINT_FILES_EXPECTED[packcode] == len(print_file_message.splitlines())

    logger.info('Time to produce print_files', runtime=str(context.produced_print_file_time
                                                           - context.action_rule_trigger_time))


def decrypt_message(message, key_file_path, key_passphrase):
    key, _ = pgpy.PGPKey.from_file(key_file_path)
    with key.unlock(key_passphrase):
        encrypted_text_message = pgpy.PGPMessage.from_blob(message)
        message_text = key.decrypt(encrypted_text_message)
        return message_text.message


def open_sftp_client():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=Config.SFTP_HOST,
                       port=int(Config.SFTP_PORT),
                       username=Config.SFTP_USERNAME,
                       key_filename=str(Path(__file__).parents[2].joinpath(Config.SFTP_KEY_FILENAME)),
                       passphrase=Config.SFTP_PASSPHRASE,
                       look_for_keys=False,
                       timeout=120)
    sftp = ssh_client.open_sftp()
    return sftp
