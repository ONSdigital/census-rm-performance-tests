from datetime import datetime, timedelta
from pathlib import Path
from time import sleep

import pgpy
from behave import step

from config import Config
from utilties.mappings import PACK_CODE_TO_SFTP_DIRECTORY, PACK_CODE_TO_ACTION_TYPE
from utilties.sftp_utility import SftpUtility


# timeout in concourse to stop it going on forever
@step('all the initial contact print files are produced on the SFTP')
def wait_for_print_files(context):
    with SftpUtility() as sftp:
        while True:
            context.all_initial_print_sftp_paths = fetch_all_print_files_paths(sftp)
            if context.all_initial_print_sftp_paths:
                context.produced_print_file_time = datetime.utcnow()
                context.print_file_production_run_time = context.produced_print_file_time \
                                                         - context.action_rule_trigger_time
                # TODO nicer way to print within behave
                print(f'\nTime from action rule trigger to all print files produced: '
                      f'[{str(context.print_file_production_run_time)}]\n')
                break
        sleep(int(Config.SFTP_POLLING_DELAY))


def fetch_all_print_files_paths(sftp):
    print_file_paths = []
    print_file_paths.extend([Path(Config.SFTP_QM_DIRECTORY).joinpath(str(file_name.filename)) for file_name in
                             sftp.get_all_print_files(Config.SFTP_QM_DIRECTORY)])
    print_file_paths.extend([Path(Config.SFTP_PPO_DIRECTORY).joinpath(str(file_name.filename)) for file_name in
                             sftp.get_all_print_files(Config.SFTP_PPO_DIRECTORY)])

    for pack_code in PACK_CODE_TO_SFTP_DIRECTORY.keys():
        matching_csv_files = [print_file_path for print_file_path in print_file_paths
                              if print_file_path.name.startswith(pack_code)
                              and print_file_path.name.endswith('.csv.gpg')]
        matching_manifest_files = [print_file_path for print_file_path in print_file_paths
                                   if print_file_path.name.startswith(pack_code)
                                   and print_file_path.name.endswith('.manifest')]
        if len(matching_csv_files) != 1 and len(matching_manifest_files) != 1:
            return []
    return print_file_paths


@step('they all have the correct line count')
def print_file_line_count(context):
    print_file_paths = [file_path for file_path in context.all_initial_print_sftp_paths
                        if file_path.name.endswith('.csv.gpg')]
    with SftpUtility() as sftp:
        for print_file_path in print_file_paths:
            with sftp.sftp_client.open(str(print_file_path)) as initial_contact_print_file:
                decrypted_print_file = decrypt_message(initial_contact_print_file.read(), Path(__file__).parents[2]
                                                       .joinpath('resources', 'dummy_keys', 'our_dummy_private.asc'),
                                                       key_passphrase='test')

        packcode = '_'.join(print_file_path.name.split('_')[0:3])
        assert context.expected_line_counts[PACK_CODE_TO_ACTION_TYPE[packcode]] == len(
            decrypted_print_file.splitlines()), f'The {packcode} file had an incorrect number of lines'


def decrypt_message(message, key_file_path, key_passphrase):
    key, _ = pgpy.PGPKey.from_file(key_file_path)
    with key.unlock(key_passphrase):
        encrypted_text_message = pgpy.PGPMessage.from_blob(message)
        message_text = key.decrypt(encrypted_text_message)
        return message_text.message


@step("they are produced within the configured time limit")
def step_impl(context):
    assert context.print_file_production_run_time < timedelta(minutes=Config.PRINT_FILE_TIME_LIMIT_MINUTES), (
        f'Print file production exceeded time limit: '
        f'limit = [{timedelta(minutes=Config.PRINT_FILE_TIME_LIMIT_MINUTES)}], '
        f'actual = [{context.print_file_production_run_time}]')
