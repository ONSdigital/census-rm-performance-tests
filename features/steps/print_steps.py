import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep

from behave import step
from structlog import wrap_logger

from config import Config
from utilties.mappings import PACK_CODE_TO_ACTION_TYPE
from utilties.sftp_utility import SftpUtility

logger = wrap_logger(logging.getLogger(__name__))


@step("all the manifest files are created with correct row count within {timeout} hours")
def manifest_files_all_created_with_correct_row_counts(context, timeout):
    timeout_start = datetime.utcnow()
    context.actual_line_counts = {action_type: 0 for action_type in context.expected_line_counts.keys()}
    context.counted_manifest_files = set()
    attempts = 0
    logger.info('Waiting for manifest files')

    with SftpUtility() as sftp:
        while True:
            context.produced_print_file_time = datetime.utcnow()
            manifest_file_sftp_paths = fetch_all_manifest_files_paths(sftp, context)
            update_actual_line_counts_from_manifest(manifest_file_sftp_paths, sftp, context)

            if context.expected_line_counts == context.actual_line_counts:
                logger.info('All print files found')
                context.print_file_production_run_time = (context.produced_print_file_time
                                                          - context.action_rule_trigger_time)
                time_taken_metric = json.dumps({
                    'event_description': 'Time from action rule trigger to all print files produced',
                    'event_type': 'ACTION_RULE_TO_PRINT',
                    'time_in_seconds': str(context.print_file_production_run_time.total_seconds()),
                    'time_taken': str(context.print_file_production_run_time),
                    'scenario_tag': context.scenario_tag
                })
                print(f'{time_taken_metric}\n')
                break
            if datetime.utcnow() - timeout_start >= timedelta(hours=int(timeout)):
                assert False, (f"Timed out waiting for print files after {timeout} hours,"
                               f" actual_line_counts: {context.actual_line_counts}")
            sleep(int(Config.SFTP_POLLING_DELAY_SECONDS))
            attempts += 1
            if not attempts % 300:
                logger.info('Still waiting for print files', current_line_counts=context.actual_line_counts)


@step("they are produced within the time limit {time_limit_minutes} minutes")
def print_file_produced_within_time_limit(context, time_limit_minutes):
    assert context.print_file_production_run_time < timedelta(minutes=int(time_limit_minutes)), (
        f'Print file production exceeded time limit: '
        f'limit = [{timedelta(minutes=time_limit_minutes)}], '
        f'actual = [{context.print_file_production_run_time}]')


def fetch_all_manifest_files_paths(sftp, context):
    manifest_file_paths = [Path(Config.SFTP_QM_DIRECTORY).joinpath(str(file_name.filename)) for file_name in
                           sftp.get_all_print_files(Config.SFTP_QM_DIRECTORY, context.test_start_local_datetime,
                                                    suffix='.manifest')]

    manifest_file_paths.extend([Path(Config.SFTP_PPO_DIRECTORY).joinpath(str(file_name.filename)) for file_name in
                                sftp.get_all_print_files(Config.SFTP_PPO_DIRECTORY, context.test_start_local_datetime,
                                                         suffix='.manifest')])
    return manifest_file_paths


def get_pack_code_from_print_file_name(print_file_name):
    for pack_code in PACK_CODE_TO_ACTION_TYPE.keys():
        if print_file_name.startswith(pack_code):
            return pack_code


def update_actual_line_counts_from_manifest(manifest_file_sftp_paths, sftp, context):
    for manifest_file_sftp_path in manifest_file_sftp_paths:
        if manifest_file_sftp_path not in context.counted_manifest_files:
            context.counted_manifest_files.add(manifest_file_sftp_path)
            manifest_data = _get_actual_manifest(sftp, str(manifest_file_sftp_path))
            pack_code = get_pack_code_from_print_file_name(manifest_file_sftp_path.name)

            context.actual_line_counts[PACK_CODE_TO_ACTION_TYPE[pack_code]] += manifest_data['files'][0]['rows']


def _get_actual_manifest(sftp_utility, manifest_file_path):
    actual_manifest_json = sftp_utility.get_file_contents_as_string(manifest_file_path)
    return json.loads(actual_manifest_json)
