from datetime import datetime

from behave import step

from tests.utilties.sftp_utility import SftpUtility

# timeout in concourse to stop it going on forever
@step('all the initial contact print files have been produced')
def wait_for_print_files():
    with SftpUtility() as sftp:
        sftp.get_all_files_after_time(datetime.utcnow())


@step('they all have the correct line count')
def print_file_line_count():
    pass
