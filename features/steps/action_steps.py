import logging
import uuid
from datetime import timedelta, datetime

from behave import step
from structlog import wrap_logger

from config import Config
from controllers.action_controller import create_action_plan, create_action_rule
logger = wrap_logger(logging.getLogger(__name__))


@step("all initial contact action rules have been scheduled in the future")
def setup_action_plan_and_rules(context):
    action_plan_url = setup_action_plan(context.action_plan_id)
    setup_action_rules(action_plan_url, action_delay=Config.ACTION_RULE_DELAY)


def setup_action_plan(action_plan_id):
    action_plan_response_body = create_action_plan(action_plan_id)

    return action_plan_response_body['_links']['self']['href']


def setup_action_rules(action_plan_url, action_delay):
    trigger_date_time = (datetime.utcnow() + timedelta(minutes=int(action_delay))).isoformat() + 'Z'
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

    for action_type, classifiers in classifiers_for_action_type.items():
        create_action_rule(str(uuid.uuid4()), trigger_date_time, classifiers,
                           action_plan_url, action_type)
