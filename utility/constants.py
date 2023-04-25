import numpy as np

updateWindow = 15                  # length of update window
nslots = 24 * 60                     # no of slots every day
updateSlots = nslots // updateWindow  # no of update slots

expected_fixed_tariff = 8
std_fixed_tariff = 2


day_temp_mean = 30
day_temp_std = 5
night_temp_mean = 20
night_temp_std = 5

eu_grid_prices = [97.7, 83.58, 82.09, 76.4, 75.08, 86.55, 114.6, 133.8, 135, 126.92, 110.81, 108.01, 98.07, 94.9, 87, 84.91, 86.92, 98.41, 117.48, 134.57, 135.97, 138, 120.91, 100.63]

eumean = np.mean(eu_grid_prices)
eustd = np.std(eu_grid_prices)
grid_prices = [expected_fixed_tariff + (std_fixed_tariff / eustd) * (x - eumean) for x in eu_grid_prices]

delta = 0.2  # Transititon to Slot length ratio
Po = 350  # Power that Thermostat works on to change 1 deg Celcius temperature in delta*updateWindow time  (J/min)
changeTime = delta * updateWindow
staticTime = (1 - delta) * updateWindow

inf = 1e7
