import os
import json
from locust import HttpLocust, TaskSet, task

class UserBehaviour(TaskSet):
    AUTH_USERNAME = 'admin'
    AUTH_PASSWORD = 'secret'
    CASE_ID = os.getenv('CASE_ID')
    HEADERS = {
        'Accepts': 'application/json',
        'Content-Type': 'application/json'
    }

    @task(2)
    def get_case(self):
        self.client.get(f"/cases/{UserBehaviour.CASE_ID}", auth=(UserBehaviour.AUTH_USERNAME, UserBehaviour.AUTH_PASSWORD), headers=UserBehaviour.HEADERS)
    
    @task(2)
    def get_case_events(self):
        self.client.get(f"/cases/{UserBehaviour.CASE_ID}/events", auth=(UserBehaviour.AUTH_USERNAME, UserBehaviour.AUTH_PASSWORD), headers=UserBehaviour.HEADERS)
    
    @task(1)
    def get_categories(self):
        self.client.get("/categories", auth=(UserBehaviour.AUTH_USERNAME, UserBehaviour.AUTH_PASSWORD), headers=UserBehaviour.HEADERS)
    
    @task(3)
    def post_case_event(self):
        event_json = {'description':'Load testing','category':'ACTION_COMPLETED','createdBy':'Locust'}
        self.client.post(f"/cases/{UserBehaviour.CASE_ID}/events", auth=(UserBehaviour.AUTH_USERNAME, UserBehaviour.AUTH_PASSWORD),
        data=json.dumps(event_json), headers=UserBehaviour.HEADERS)

class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    min_wait = int(os.getenv('MIN_WAIT_TIME_MS', 1000))
    max_wait = int(os.getenv('MAX_WAIT_TIME_MS', 10000))
