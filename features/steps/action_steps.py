import csv
import uuid
from datetime import timedelta, datetime
from time import sleep

from behave import step

from config import Config
from controllers.action_controller import create_action_plan, create_action_rule


@step("all initial contact action rules have been scheduled in the future")
def setup_action_plan_and_rules(context):
    action_plan_url = setup_action_plan(context.action_plan_id)
    setup_action_rules(context, action_plan_url, action_rule_delay=Config.ACTION_RULE_DELAY_MINUTES)


def setup_action_plan(action_plan_id):
    action_plan_response_body = create_action_plan(action_plan_id)

    return action_plan_response_body['_links']['self']['href']


def get_treatment_code_to_ic_action_type(classifiers_for_action_type):
    treatment_code_to_ic_action_type = {}
    for action_type, classifiers in classifiers_for_action_type.items():
        for treatment_code in classifiers['treatmentCode']:
            treatment_code_to_ic_action_type[treatment_code] = action_type
    return treatment_code_to_ic_action_type


def get_expected_line_counts(sample_file_path, classifiers_for_action_type):
    expected_line_counts = {action_type: 0 for action_type in classifiers_for_action_type}
    treatment_code_to_action_type = get_treatment_code_to_ic_action_type(classifiers_for_action_type)
    with open(sample_file_path) as sample_file:
        reader = csv.DictReader(sample_file)
        for row in reader:
            expected_line_counts[treatment_code_to_action_type[row['TREATMENT_CODE']]] += 1

    # TODO nicer way to print within behave
    print(f'Expected line counts for each action type: {expected_line_counts}\n')
    return expected_line_counts


def setup_action_rules(context, action_plan_url, action_rule_delay):
    context.action_rule_trigger_time = datetime.utcnow() + timedelta(minutes=action_rule_delay)
    trigger_date_time = context.action_rule_trigger_time.isoformat() + 'Z'
    classifiers_for_action_type = {
        'ICL1E': {'treatmentCode': ['HH_LF2R1E', 'HH_LF2R2E', 'HH_LF2R3AE', 'HH_LF2R3BE', 'HH_LF3R1E', 'HH_LF3R2E',
                                    'HH_LF3R3AE', 'HH_LF3R3BE', 'HH_LFNR1E', 'HH_LFNR2E', 'HH_LFNR3AE', 'HH_LFNR3BE']},
        'ICL2W': {'treatmentCode': ['HH_LF2R1W', 'HH_LF2R2W', 'HH_LF2R3AW', 'HH_LF2R3BW', 'HH_LF3R1W', 'HH_LF3R2W',
                                    'HH_LF3R3AW', 'HH_LF3R3BW', 'HH_LFNR1W', 'HH_LFNR2W', 'HH_LFNR3AW', 'HH_LFNR3BW']},
        'ICL4N': {'treatmentCode': ['HH_1LSFN', 'HH_2LEFN']},
        'ICHHQE': {'treatmentCode': ['HH_QF2R1E', 'HH_QF2R2E', 'HH_QF2R3AE', 'HH_QF3R1E', 'HH_QF3R2E', 'HH_QF3R3AE',
                                     'HH_QFNR1E', 'HH_QFNR2E', 'HH_QFNR3AE']},
        'ICHHQW': {'treatmentCode': ['HH_QF2R1W', 'HH_QF2R2W', 'HH_QF2R3AW', 'HH_QF3R1W', 'HH_QF3R2W', 'HH_QF3R3AW',
                                     'HH_QFNR1W', 'HH_QFNR2W', 'HH_QFNR3AW']},
        'ICHHQN': {'treatmentCode': ['HH_3QSFN']}
    }
    context.expected_line_counts = get_expected_line_counts(Config.SAMPLE_FILE_PATH, classifiers_for_action_type)
    for action_type, classifiers in classifiers_for_action_type.items():
        create_action_rule(str(uuid.uuid4()), trigger_date_time, classifiers,
                           action_plan_url, action_type)


@step("the action rules trigger")
def wait_for_action_rule_trigger(context):
    wait_seconds = (context.action_rule_trigger_time - datetime.utcnow()).total_seconds()
    print(f'Waiting {wait_seconds / 60} minutes for action rules to trigger '
          f'at {context.action_rule_trigger_time.time()} UTC\n')
    sleep(wait_seconds)
