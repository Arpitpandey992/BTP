import os
from time import sleep
import requests

api_key = os.environ['API_KEY_THINGSPEAK']
sleep_time = 1 * 60


def request(url: str):
    response = '0'
    retries_left = 200
    while retries_left > 0:
        response = requests.get(url).text
        retries_left -= 1
        if response != '0':
            break
    if response == '0':
        print("Thingspeak API hit failed due to retries exceeded")
    return response
