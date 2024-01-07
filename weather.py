from typing import NamedTuple


class Weather(NamedTuple):
    description: str
    temp: float
    feels_like: float
    date: str
