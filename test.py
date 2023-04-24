from utility.pso import test_pso
from utility.adam import test_adam
from dotenv import load_dotenv

from weather.temperature import get_temperature_values

load_dotenv()

temp = get_temperature_values()
print(temp)
test_pso()
test_adam()
