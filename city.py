import requests

from coordinates import Coordinates
from weather import Weather


class City:

    def __init__(self, name: str, api: str) -> None:
        self.name: str = self.get_local_name(name, api)
        self.api: str = api
        self.coord: Coordinates = self.get_geocodng(name, api)

    @staticmethod
    def get_local_name(name: str, api: str) -> str:
        response_json = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q=' +
                                     f'{name}&limit=5&appid={api}').json()[0]
        return response_json['local_names']['ru']

    @staticmethod
    def get_geocodng(city_name: str, api_key: str) -> Coordinates:
        response_json = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?' +
            f'q={city_name}&limit=1&appid={api_key}').json()[0]
        lat = float(response_json['lat'])
        lon = float(response_json['lon'])
        return Coordinates(lat, lon)

    @staticmethod
    def check_city_name(city_name: str, api_key: str) -> bool:
        response_json = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?' +
            f'q={city_name}&limit=1&appid={api_key}').json()
        return len(response_json) != 0

    def get_curr_weather(self) -> Weather:
        response_json = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={self.coord.lat}&lon={self.coord.lon}' +
            f'&appid={self.api}&lang=ru&units=metric').json()
        description = response_json['weather'][0]['description'].capitalize()
        temp = float(response_json['main']['temp'])
        feels_like = float(response_json['main']['feels_like'])
        return Weather(description, temp, feels_like, "now")

    def get_more_weather(self) -> list[Weather]:
        weathers = []
        response_json = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?' +
                                     f'lat={self.coord.lat}&lon={self.coord.lon}&appid={self.api}' +
                                     f'&lang=ru&units=metric').json()['list']
        for info in response_json:
            description = info['weather'][0]['description'].capitalize()
            temp = float(info['main']['temp'])
            feels_like = float(info['main']['feels_like'])
            date = info['dt_txt']
            weathers.append(Weather(description, temp, feels_like, date))
        return weathers

    def show_city(self) -> None:
        weather = self.get_curr_weather()
        print(f'Город: {self.name}\n' +
              f'\tОписание погоды: {weather.description}, текущая температура: {weather.temp}, ' +
              f'ощущается как: {weather.feels_like}')
