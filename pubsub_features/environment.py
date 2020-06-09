import base64
import json

from config import Config


def before_all(_context):
    _setup_google_auth()


def before_scenario(context, scenario):
    assert len(scenario.effective_tags) == 1, 'Unexpected scenario tags'
    context.scenario_tag = scenario.effective_tags[0]


def _setup_google_auth():
    if Config.GOOGLE_SERVICE_ACCOUNT_JSON and Config.GOOGLE_APPLICATION_CREDENTIALS:
        sa_json = json.loads(base64.b64decode(Config.GOOGLE_SERVICE_ACCOUNT_JSON))
        with open(Config.GOOGLE_APPLICATION_CREDENTIALS, 'w') as credentials_file:
            json.dump(sa_json, credentials_file)
        print(f'Created GOOGLE_APPLICATION_CREDENTIALS: {Config.GOOGLE_APPLICATION_CREDENTIALS}')
