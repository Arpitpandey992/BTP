import os
import requests


def get_latiture_longitude(city: str) -> tuple[float, float]:
    api_key_openweather = os.environ.get('API_KEY_OPENWEATHER')
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key_openweather}"
    response = requests.get(url).json()
    return response[0]['lat'], response[0]['lon']


def get_weather_values(city: str) -> list:
    api_key_pirate = os.environ.get('API_KEY_PIRATE')
    lat, lon = get_latiture_longitude(city)
    url = f"https://api.pirateweather.net/forecast/{api_key_pirate}/{lat},{lon}?extend=hourly&exclude=minutely,daily,currently,alerts&units=si"
    response = requests.get(url)
    response = response.json()
    return [resp for resp in response['hourly']['data'][:96]]


if __name__ == '__main__':
    print(get_weather_values('Roorkee'))
