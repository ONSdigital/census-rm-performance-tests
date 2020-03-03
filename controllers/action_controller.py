import logging

import requests
from structlog import wrap_logger

from config import Config

logger = wrap_logger(logging.getLogger(__name__))


def create_action_plan(action_plan_id):
    # logger.debug('Creating action plan')
    #
    # url = f'{Config.ACTION_SERVICE}/actionPlans'
    #
    # body = {'id': action_plan_id}
    #
    # # response = requests.post(url, json=body)

    url = f'{Config.ACTION_SERVICE}/actionPlans/{action_plan_id}'

    response = requests.get(url=url)

    response.raise_for_status()

    logger.debug('Successfully created action plan')

    return response.json()


def create_action_rule(action_rule_id, trigger_date_time, classifiers, action_plan_url, action_type,
                       has_triggered=False):
    logger.debug('Creating action rule')

    url = f'{Config.ACTION_SERVICE}/actionRules'

    body = {'id': action_rule_id, 'triggerDateTime': trigger_date_time, 'classifiers': classifiers,
            'actionPlan': action_plan_url, 'actionType': action_type, 'hasTriggered': has_triggered}

    response = requests.post(url, json=body)

    response.raise_for_status()

    logger.debug('Successfully created action rule')

    return response.json()
