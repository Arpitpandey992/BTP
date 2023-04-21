from weather.utils import get_weather_values

DEFAULT_CITY = 'Roorkee'


def get_temperature_values(city: str = DEFAULT_CITY) -> list[float]:
    weather_values = get_weather_values(city)
    temperature_values = list()
    for i in range(24):
        temperature_values.extend([
            weather_values[i]['temperature'],
            weather_values[i + 24]['temperature'],
            weather_values[i + 48]['temperature'],
            weather_values[i + 72]['temperature'],
        ])
    return temperature_values


if __name__ == '__main__':
    get_temperature_values()
