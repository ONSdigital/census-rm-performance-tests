import uuid
from datetime import timedelta, datetime
from pathlib import Path

from load_sample import load_sample_file

from config import Config
from tests.controllers.action_controller import create_action_rule, create_action_plan

variables = {'action_plan_id': str(uuid.uuid4()),
             'collection_exercise_id': str(uuid.uuid4())}


def print_files_created():


def checking_print_file_line_length():


def starting_performance_test():
    setup_action_plan()
    loading_sample()
    print_files_created()
    checking_print_file_line_length()
    send_results_to_gcp()



if __name__ == '__main__':
    starting_performance_test()