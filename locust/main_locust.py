from locust import HttpUser, task, between, events 
import requests
import os
from locust.exception import StopUser
from get_env_path import load_all_env
from login import login_attempt
from move_cart import move_cart
from bulk_update_quantity import bulk_update_cart_quantity

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    load_all_env()
    
    session = requests.Session()
    session.headers.update({"user-agent" : os.environ.get("USER_AGENT")})
    session.headers.update({"content-type" : os.environ.get("CONTENT_TYPE")})
    
    login_attempt(session)
    move_cart(session)
    environment.shared_session = session


class KurlyUserScenario(HttpUser):
    wait_time = between(0.01,0.02)
    host = "https://www.kurly.com"

    def on_start(self):
        self.session = getattr(self.environment, "shared_session")
    
    @task
    def kurly_concurrency_scenario(self):
        bulk_update_cart_quantity(self)

        raise StopUser()
        

