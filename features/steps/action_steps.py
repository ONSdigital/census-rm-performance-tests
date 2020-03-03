import csv
import uuid
from datetime import datetime

from behave import step

from controllers.action_controller import create_action_plan, create_action_rule


@step("all initial contact action rules are scheduled for now")
def setup_action_plan_and_rules(context):
    context.action_plan_id = 'a2656051-2fef-47e6-8a86-2c8521535bbf'
    context.sample_file = 'sample_file_from_bucket.csv'
    action_plan_url = setup_action_plan(context.action_plan_id)
    setup_action_rules(context, action_plan_url)


def setup_action_plan(action_plan_id):
    action_plan_response_body = create_action_plan(action_plan_id)
    return action_plan_response_body['_links']['self']['href']


def get_treatment_code_to_ic_action_type(classifiers_for_action_type):
    treatment_code_to_ic_action_type = {}
    for action_type, classifiers in classifiers_for_action_type.items():
        for treatment_code in classifiers['treatment_code']:
            treatment_code_to_ic_action_type[treatment_code] = action_type
    return treatment_code_to_ic_action_type


def get_expected_line_counts(sample_file_path, classifiers_for_action_type):
    expected_line_counts = {action_type: 0 for action_type in classifiers_for_action_type}
    treatment_code_to_action_type = get_treatment_code_to_ic_action_type(classifiers_for_action_type)
    with open(sample_file_path) as sample_file:
        reader = csv.DictReader(sample_file)
        for row in reader:
            action_type = treatment_code_to_action_type.get(row['TREATMENT_CODE'])
            if action_type:
                expected_line_counts[action_type] += 1

    # TODO nicer way to print within behave
    print(f'Expected line counts for each action type: {expected_line_counts}\n')
    return expected_line_counts


def setup_action_rules(context, action_plan_url):
    context.action_rule_trigger_time = datetime.utcnow()
    trigger_date_time = context.action_rule_trigger_time.isoformat() + 'Z'
    classifiers_for_action_type = {
        'ICL1E': {'treatment_code': ['HH_LF2R1E', 'HH_LF2R2E', 'HH_LF2R3AE', 'HH_LF2R3BE', 'HH_LF3R1E', 'HH_LF3R2E',
                                     'HH_LF3R3AE', 'HH_LF3R3BE', 'HH_LFNR1E', 'HH_LFNR2E', 'HH_LFNR3AE', 'HH_LFNR3BE']},
        'ICL2W': {'treatment_code': ['HH_LF2R1W', 'HH_LF2R2W', 'HH_LF2R3AW', 'HH_LF2R3BW', 'HH_LF3R1W', 'HH_LF3R2W',
                                     'HH_LF3R3AW', 'HH_LF3R3BW', 'HH_LFNR1W', 'HH_LFNR2W', 'HH_LFNR3AW', 'HH_LFNR3BW']},
        'ICL4N': {'treatment_code': ['HH_1LSFN', 'HH_2LEFN']},
        'ICHHQE': {'treatment_code': ['HH_QF2R1E', 'HH_QF2R2E', 'HH_QF2R3AE', 'HH_QF3R1E', 'HH_QF3R2E', 'HH_QF3R3AE',
                                      'HH_QFNR1E', 'HH_QFNR2E', 'HH_QFNR3AE']},
        'ICHHQW': {'treatment_code': ['HH_QF2R1W', 'HH_QF2R2W', 'HH_QF2R3AW', 'HH_QF3R1W', 'HH_QF3R2W', 'HH_QF3R3AW',
                                      'HH_QFNR1W', 'HH_QFNR2W', 'HH_QFNR3AW']},
        'ICHHQN': {'treatment_code': ['HH_3QSFN']}
    }
    context.expected_line_counts = get_expected_line_counts(context.sample_file, classifiers_for_action_type)
    for action_type, classifiers in classifiers_for_action_type.items():
        create_action_rule(str(uuid.uuid4()), trigger_date_time, classifiers,
                           action_plan_url, action_type)
