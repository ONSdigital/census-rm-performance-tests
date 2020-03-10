import json
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep

from behave import step

from config import Config
from utilties.decrypt import decrypt_message
from utilties.mappings import PACK_CODE_TO_ACTION_TYPE
from utilties.sftp_utility import SftpUtility


def get_pack_code_from_print_file_name(print_file_name):
    for pack_code in PACK_CODE_TO_ACTION_TYPE.keys():
        if print_file_name.startswith(pack_code):
            return pack_code


def update_actual_line_counts(print_file_sftp_paths, sftp, context):
    for print_file_sftp_path in print_file_sftp_paths:
        if print_file_sftp_path not in context.counted_print_files:
            context.counted_print_files.add(print_file_sftp_path)
            pack_code = get_pack_code_from_print_file_name(print_file_sftp_path.name)

            with sftp.sftp_client.open(str(print_file_sftp_path)) as print_file:
                decrypted_print_file = decrypt_message(print_file.read(),
                                                       private_key_file_path=Config.DECRYPTION_KEY_PATH,
                                                       private_key_passphrase=Config.DECRYPTION_KEY_PASSPHRASE)
            context.actual_line_counts[PACK_CODE_TO_ACTION_TYPE[pack_code]] += len(decrypted_print_file.splitlines())


@step('all the initial contact print files are produced on the SFTP '
      'containing the correct total number of cases within {timeout} hours')
@step('all the initial contact print files are produced on the SFTP '
      'containing the correct total number of cases within {timeout} hour')
def wait_for_print_files(context, timeout):
    timeout_start = datetime.utcnow()
    context.actual_line_counts = {action_type: 0 for action_type in context.expected_line_counts.keys()}
    context.counted_print_files = set()
    with SftpUtility() as sftp:
        while True:
            context.all_initial_print_sftp_paths = fetch_all_print_files_paths(sftp, context)
            context.produced_print_file_time = datetime.utcnow()
            print_file_sftp_paths = [print_file_path for print_file_path in context.all_initial_print_sftp_paths
                                     if print_file_path.name.endswith('.csv.gpg')]
            update_actual_line_counts(print_file_sftp_paths, sftp, context)
            if context.expected_line_counts == context.actual_line_counts:
                context.print_file_production_run_time = context.produced_print_file_time \
                                                         - context.action_rule_trigger_time
                time_taken_metric = json.dumps({
                    'event_description': 'Time from action rule trigger to all print files produced',
                    'event_type': 'ACTION_RULE_TO_PRINT',
                    'time_in_seconds': str(context.print_file_production_run_time.total_seconds()),
                    'time_taken': str(context.print_file_production_run_time),
                        'scenario_label': context.scenario_tag
                })
                print(f'{time_taken_metric}\n')
                break
            if datetime.utcnow() - timeout_start >= timedelta(hours=int(timeout)):
                assert False, (f"Timed out waiting for print files after {timeout} hours,"
                               f" actual_line_counts: {context.actual_line_counts}")
        sleep(int(Config.SFTP_POLLING_DELAY_SECONDS))


def fetch_all_print_files_paths(sftp, context):
    print_file_paths = [Path(Config.SFTP_QM_DIRECTORY).joinpath(str(file_name.filename)) for file_name in
                        sftp.get_all_print_files(Config.SFTP_QM_DIRECTORY, context.test_start_local_datetime)]
    print_file_paths.extend([Path(Config.SFTP_PPO_DIRECTORY).joinpath(str(file_name.filename)) for file_name in
                             sftp.get_all_print_files(Config.SFTP_PPO_DIRECTORY, context.test_start_local_datetime)])
    return print_file_paths


@step("they are produced within the time limit {time_limit_minutes} minutes")
def print_file_produced_within_time_limit(context, time_limit_minutes):
    assert context.print_file_production_run_time < timedelta(minutes=int(time_limit_minutes)), (
        f'Print file production exceeded time limit: '
        f'limit = [{timedelta(minutes=time_limit_minutes)}], '
        f'actual = [{context.print_file_production_run_time}]')
