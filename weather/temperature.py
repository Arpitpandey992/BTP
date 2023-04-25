from weather.utils import get_weather_values

DEFAULT_CITY = 'Roorkee'


def interpolate_between(val1: float, val2: float, num_values: int) -> list[float]:
    return [val1 + (val2 - val1) * i / (num_values - 1) for i in range(num_values)]


def get_temperature_values(city: str = DEFAULT_CITY) -> list[float]:
    weather_values = get_weather_values(city)
    temperature_values = list()
    for i in range(len(weather_values) - 1):
        current_temperature = weather_values[i]['temperature']
        next_temperature = weather_values[i + 1]['temperature']
        values = interpolate_between(current_temperature, next_temperature, 5)
        temperature_values.extend(values[:-1])
    return temperature_values
