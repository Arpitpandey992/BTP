from time import sleep
import numpy as np
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import threading

from dotenv import load_dotenv
load_dotenv()

import utility.thingspeak as thingspeak
from utility.adam import grad_descent
from utility.constants import grid_prices
from utility.cost_utils import overall_price_function
from weather.temperature import get_temperature_values


def createApp(testing: bool = True):
    app = Flask(__name__)
    CORS(app)
    alphas = np.linspace(0, 1, 11)
    alphas[-1] = 0.99

    # Routes
    @app.route('/adam', methods=['GET'])
    def apply_adam():
        Tmin, Tset, Tmax = int(request.args.get('tmin')), int(request.args.get('tset')), int(request.args.get('tmax'))  # type: ignore
        print(f"GET apply_adam - Tmin:{Tmin}, Tset:{Tset}, Tmax:{Tmax}")
        print("Getting external temperatures")
        external_temperatures = get_temperature_values()
        adam_output = list()
        for alpha in alphas:
            room_temperatures = grad_descent(alpha, external_temperatures, Tmin, Tset, Tmax).tolist()
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
        try:
            if not response:
                raise (Exception('Empty Body'))
            alpha = response['alpha']
            Tmin = int(response['tmin'])
            Tset = int(response['tset'])
            Tmax = int(response['tmax'])
        except Exception as e:
            print(f"Exception in select alpha -> {e}")
            abort(400, f'{e} Key missing')
        print(f"POST select alpha - alpha:{alpha}, Tmin:{Tmin}, Tset:{Tset}, Tmax:{Tmax}")
        alpha = min(alpha, 0.99)
        alpha = max(alpha, 0)
        print("Getting external temperatures")
        external_temperatures = get_temperature_values()
        room_temperatures = grad_descent(alpha, external_temperatures, Tmin, Tset, Tmax).tolist()
        step_size = 4

        def async_select_alpha():
            for i in range(0, len(room_temperatures), step_size):
                current_temperature = room_temperatures[i]
                thingspeak_api_url = f"https://api.thingspeak.com/update?api_key={thingspeak.api_key}&field3={Tmax}&field4={Tmin}&field5={Tset}&field6={current_temperature}"
                response = thingspeak.request(thingspeak_api_url)
                print(f"Updated thingspeak dashboard - Tmin:{Tmin}, Tset:{Tset}, Tmax:{Tmax}, Tcur:{current_temperature}, response = {response}")
                sleep(thingspeak.sleep_time)
        update_time = f"{thingspeak.sleep_time} seconds" if thingspeak.sleep_time <= 60 else f"{thingspeak.sleep_time/60} minutes"
        print(f"updating thingsSpeak dashboard every {update_time} minutes, step size: {step_size}")
        threading.Thread(target=async_select_alpha).start()
        return {
            'status': 200,
            'message': f'started updating thingspeak dashboard every {thingspeak.sleep_time} seconds',
            'external_temperatures': external_temperatures,
            'room_temperatures': room_temperatures
        }

    return app


if __name__ == '__main__':
    app = createApp(testing=True)
    app.run(debug=True, port=8000)
