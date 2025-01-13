import random
from faker.providers import BaseProvider
from faker import Faker
import config
import time
import requests
import json
import uuid

# Define a TaskProvider
class TaskProvider(BaseProvider):
    def task_priority(self):
        severity_levels = ['Low', 'Moderate', 'Major', 'Critical']
        return severity_levels[random.randint(0, len(severity_levels) - 1)]

# Create a Faker instance and seed it to have the same results every time we execute the script
fakeTasks = Faker('en_US')
# Seed the Faker instance to have reproducible results
fakeTasks.seed_instance(0)
# Add the TaskProvider to the Faker instance
fakeTasks.add_provider(TaskProvider)

# Generate a Fake Task
def produce_task(batchid, taskid):
    message = {
        'batchid': batchid,
        'id': taskid,
        'owner': fakeTasks.unique.name(),
        'priority': fakeTasks.task_priority()
        # Uncomment the following lines if you want to add more details
        # 'raised_date': fakeTasks.date_time_this_year(),
        # 'description': fakeTasks.text()
    }
    return message

def send_webhook(msg):
    """
    Send a webhook to a specified URL
    :param msg: task details
    :return: Response status code
    """
    try:
        # Post a webhook message
        resp = requests.post(
            config.WEBHOOK_RECEIVER_URL,
            data=json.dumps(msg, sort_keys=True, default=str),
            headers={'Content-Type': 'application/json'},
            timeout=1.0
        )
        resp.raise_for_status()
        return resp.status_code
    except requests.exceptions.HTTPError as err:
        print("An HTTP Error occurred:", repr(err))
    except requests.exceptions.ConnectionError as err:
        print("An Error Connecting to the API occurred:", repr(err))
    except requests.exceptions.Timeout as err:
        print("A Timeout Error occurred:", repr(err))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred:", repr(err))
    return None

def produce_bunch_tasks():
    """
    Generate a Bunch of Fake Tasks
    """
    try:
        n = random.randint(config.MIN_NBR_TASKS, config.MAX_NBR_TASKS)
        batchid = str(uuid.uuid4())

        for i in range(n):
            msg = produce_task(batchid, i)
            status_code = send_webhook(msg)
            print(i + 1, "out of", n, "-- Status Code:", status_code, "-- Message:", msg)
            time.sleep(config.WAIT_TIME)
            yield status_code, n, msg
    except Exception as err:
        print("An error occurred while producing tasks:", repr(err))

if __name__ == "__main__":
    for resp, total, msg in produce_bunch_tasks():
        pass
