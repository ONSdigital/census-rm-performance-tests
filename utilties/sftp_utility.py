from datetime import datetime

import paramiko

from config import Config


class SftpUtility:
    def __init__(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.ssh_client.connect(hostname=Config.SFTP_HOST,
                                port=int(Config.SFTP_PORT),
                                username=Config.SFTP_USERNAME,
                                key_filename=str(Config.SFTP_SSH_KEY_PATH),
                                passphrase=Config.SFTP_PASSPHRASE,
                                look_for_keys=False,
                                timeout=120)

    def __enter__(self):
        self.sftp_client = self.ssh_client.open_sftp()
        return self

    def __exit__(self, *_):
        self.ssh_client.close()

    def get_all_print_files(self, sftp_directory, period_start_time, prefix='', suffix='', ):
        files = self.sftp_client.listdir_attr(sftp_directory)

        return [
            _file for _file in files
            if f'{prefix}' in _file.filename
               and _file.filename.endswith(suffix)
               and period_start_time <= datetime.fromtimestamp(_file.st_mtime)
        ]

    def get_file_contents_as_string(self, file_path):
        with self.sftp_client.open(file_path) as sftp_file:
            return sftp_file.read().decode('utf-8')

