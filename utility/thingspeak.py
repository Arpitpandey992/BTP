import os
from time import sleep
import requests

api_key = os.environ['API_KEY_THINGSPEAK']
sleep_time = 15 * 60


def request(url: str):
    response = 0
    retries_left = 20
    while retries_left > 0:
        response = requests.get(url)
        retries_left -= 1
        if response == 0:
            sleep(1)
        else:
            break
    print(f'Thingspeak API called - {url}')
    return response
