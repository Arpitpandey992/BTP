import os
from time import sleep
import numpy as np
from flask import Flask, request, abort, send_file
from flask_cors import CORS
import threading
import uuid

from dotenv import load_dotenv
from utility.plot import plot_temp_vs_time
load_dotenv()

import utility.thingspeak as thingspeak
from utility.adam import grad_descent
from utility.constants import grid_prices
from utility.cost_utils import overall_price_function
from weather.temperature import get_temperature_values


thread_number = 1


def createApp(testing: bool = True):
    app = Flask(__name__)
    CORS(app)
    alphas = np.linspace(0, 1, 11)
    alphas[-1] = 0.99

    # Routes
    @app.route('/adam', methods=['GET'])
    def apply_adam():
        Tmin, Tset, Tmax = float(request.args.get('tmin')), float(request.args.get('tset')), float(request.args.get('tmax'))  # type: ignore
        print(f"GET apply_adam - Tmin:{Tmin}, Tset:{Tset}, Tmax:{Tmax}")
        print("Getting external temperatures")
        external_temperatures = get_temperature_values()
        adam_output = list()
        plot_id = uuid.uuid1()
        plot_base_path = os.path.join("plots", str(plot_id))
        while os.path.exists(plot_base_path):
            plot_id = uuid.uuid1()
            plot_base_path = os.path.join("plots", str(plot_id))
        os.makedirs(plot_base_path)
        for index, alpha in enumerate(alphas):
            room_temperatures = grad_descent(alpha, external_temperatures, Tmin, Tset, Tmax).tolist()
            plot_path = os.path.join(plot_base_path, f"{index}.png")
            plot_temp_vs_time(external_temperatures, room_temperatures, plot_path)
            overall_price = overall_price_function(grid_prices, room_temperatures, external_temperatures)
            adam_output.append({
                'alpha': alpha,
                'room_temperatures': room_temperatures,
                'overall_price': overall_price,
                'plot_location': plot_path
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
            Tset = float(response['tset'])
            Tmin = float(response['tmin'])
            Tmax = float(response['tmax'])
            manual_mode = bool(response.get('manual_mode', False))
        except Exception as e:
            print(f"Exception in select alpha -> {e}")
            abort(400, f'{e} Key missing')
        print(f"POST select alpha - alpha:{alpha}, Tmin:{Tmin}, Tset:{Tset}, Tmax:{Tmax}")
        alpha = min(alpha, 0.99)
        alpha = max(alpha, 0)
        print("Getting external temperatures")
        external_temperatures = get_temperature_values()
        room_temperatures = grad_descent(alpha, external_temperatures, Tmin, Tset, Tmax).tolist()
        step_size = 8

        def async_select_alpha():
            global thread_number
            current_thread_number = thread_number + 1
            thread_number = current_thread_number
            loop_range = 1 if manual_mode else len(room_temperatures)
            for i in range(0, loop_range, step_size):
                if thread_number != current_thread_number:
                    print(f"thread with id = {current_thread_number} killed")
                    return
                current_temperature = room_temperatures[i]
                if manual_mode:
                    thingspeak_api_url = f"https://api.thingspeak.com/update?api_key={thingspeak.api_key}&field3={Tmax}&field4={Tmin}&field5={Tset}&field6={Tset}"
                else:
                    thingspeak_api_url = f"https://api.thingspeak.com/update?api_key={thingspeak.api_key}&field3={Tmax}&field4={Tmin}&field5={Tset}&field6={current_temperature}"
                response = thingspeak.request(thingspeak_api_url)
                print(f"Updated thingspeak dashboard - Tmin:{Tmin}, Tset:{Tset}, Tmax:{Tmax}, Tcur:{current_temperature if not manual_mode else Tset}, response = {response}")
                sleep(thingspeak.sleep_time)
            print('Done')
        update_time = f"{thingspeak.sleep_time} seconds" if thingspeak.sleep_time <= 60 else f"{thingspeak.sleep_time/60} minutes"
        print(f"updating thingsSpeak dashboard every {update_time}, step size: {step_size}")
        threading.Thread(target=async_select_alpha).start()
        return {
            'status': 200,
            'message': f'started updating thingspeak dashboard every {thingspeak.sleep_time} seconds',
            'external_temperatures': external_temperatures,
            'room_temperatures': room_temperatures
        }

    @app.route('/<path:path>')
    def serve_images(path):
        print(f'Image request : {path}')
        return send_file(path)

    return app


if __name__ == '__main__':
    app = createApp(testing=True)
    app.run(debug=True, port=8000)
