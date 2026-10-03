from dataclasses import dataclass
from typing import List


@dataclass
class Location:
    name: str
    country: str
    latitude: float
    longitude: float
    timezone: str


@dataclass
class CurrentWeather:
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    weather_code: int
    is_day: bool
    local_time: str


@dataclass
class DailyForecast:
    date: str
    weather_code: int
    temperature_max: float
    temperature_min: float
    precipitation_probability: int
    sunrise: str
    sunset: str


@dataclass
class WeatherData:
    location: Location
    current: CurrentWeather
    forecast: List[DailyForecast]