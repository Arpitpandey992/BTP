from time import sleep
import numpy as np
import requests
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv

import utility.thingspeak as thingspeak
from utility.adam import grad_descent
from utility.constants import grid_prices
from utility.cost_utils import overall_price_function
from weather.temperature import get_temperature_values


def createApp(testing: bool = True):
    app = Flask(__name__)
    CORS(app)
    load_dotenv()
    alphas = np.linspace(0, 1, 11)

    # Routes
    # adam @alpha 0-1, overall_price_fn
    @app.route('/adam', methods=['GET'])
    def apply_adam():
        external_temperatures = get_temperature_values()
        Tmin, Tset, Tmax = request.args.get('tmin'), request.args.get('tset'), request.args.get('tmax')
        adam_output = list()
        for alpha in alphas:
            room_temperatures = grad_descent(alpha, external_temperatures, Tmin, Tset, Tmax)
            overall_price = overall_price_function(grid_prices, room_temperatures, external_temperatures)
            adam_output.append({
                'alpha': alpha,
                'room_temperatures': room_temperatures,
                'overall_price': overall_price
            })
        return {
            'external_temperatures': external_temperatures,
            'adam_output': adam_output
        }

    @app.route('/select_alpha', methods=['POST'])
    def select_alpha():
        response = request.json
        if not response:
            return {"400": "Bad Request"}
        alpha = response['alpha']
        Tmin = response['tmin']
        Tset = response['tset']
        Tmax = response['tmax']
        external_temperatures = get_temperature_values()
        room_temperatures = grad_descent(alpha, external_temperatures, Tmin, Tset, Tmax)
        # hit the thingsSpeak API every 15 minutes
        for current_temperature in room_temperatures:
            thing_speak_api_url = f"api.thingspeak.com/update?api_key=DXAHHTGT4Y0XL1GE&field3={Tmax}&field4={Tmin}&field5={Tset}&field6={current_temperature}"
            thingspeak.request(thing_speak_api_url)
            sleep(15)
        return {"200": "Success"}
    return app

if __name__ == '__main__':
    app = createApp(testing=True)
    app.run()
