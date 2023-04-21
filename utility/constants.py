from utility.utils import generate_array_for_mean_and_std

updateWindow = 15                  # length of update window
nslots = 24 * 60                     # no of slots every day
updateSlots = nslots // updateWindow  # no of update slots

expected_fixed_tariff = 8
std_fixed_tariff = 2


day_temp_mean = 30
day_temp_std = 5
night_temp_mean = 20
night_temp_std = 5

grid_prices = generate_array_for_mean_and_std(nslots // 60, expected_fixed_tariff, std_fixed_tariff)

delta = 0.2  # Transititon to Slot length ratio
Po = 350  # Power that Thermostat works on to change 1 deg Celcius temperature in delta*updateWindow time  (J/min)
changeTime = delta * updateWindow
staticTime = (1 - delta) * updateWindow

inf = 1e7
