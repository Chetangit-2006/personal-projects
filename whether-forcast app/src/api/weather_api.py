import requests

from src.models.weather_model import (
    CurrentWeather,
    DailyForecast,
    Location,
    WeatherData,
)


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherAPIError(Exception):
    """Raised when the weather API cannot return valid data."""


class WeatherAPI:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def search_location(self, city: str) -> Location:
        params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        }

        try:
            response = requests.get(
                GEOCODING_URL,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise WeatherAPIError(
                "Unable to connect to the weather service."
            ) from exc

        results = data.get("results")

        if not results:
            raise WeatherAPIError(
                f"Could not find a location named '{city}'."
            )

        result = results[0]

        return Location(
            name=result.get("name", city),
            country=result.get("country", "Unknown"),
            latitude=float(result["latitude"]),
            longitude=float(result["longitude"]),
            timezone=result.get("timezone", "auto"),
        )

    def get_weather(self, city: str) -> WeatherData:
        location = self.search_location(city)

        params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "is_day,"
                "weather_code,"
                "wind_speed_10m"
            ),
            "daily": (
                "weather_code,"
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_probability_max,"
                "sunrise,"
                "sunset"
            ),
            "forecast_days": 7,
            "timezone": "auto",
        }

        try:
            response = requests.get(
                FORECAST_URL,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise WeatherAPIError(
                "Unable to retrieve weather information."
            ) from exc

        return self._parse_weather_data(data, location)

    def _parse_weather_data(
        self,
        data: dict,
        location: Location,
    ) -> WeatherData:

        current_data = data.get("current")

        if not current_data:
            raise WeatherAPIError(
                "The weather service returned incomplete current data."
            )

        daily_data = data.get("daily", {})

        current = CurrentWeather(
            temperature=float(current_data["temperature_2m"]),
            feels_like=float(current_data["apparent_temperature"]),
            humidity=int(current_data["relative_humidity_2m"]),
            wind_speed=float(current_data["wind_speed_10m"]),
            weather_code=int(current_data["weather_code"]),
            is_day=bool(current_data["is_day"]),
            local_time=current_data.get("time", ""),
        )

        dates = daily_data.get("time", [])

        forecast = []

        for index, date in enumerate(dates):
            forecast.append(
                DailyForecast(
                    date=date,
                    weather_code=int(
                        daily_data["weather_code"][index]
                    ),
                    temperature_max=float(
                        daily_data["temperature_2m_max"][index]
                    ),
                    temperature_min=float(
                        daily_data["temperature_2m_min"][index]
                    ),
                    precipitation_probability=int(
                        daily_data[
                            "precipitation_probability_max"
                        ][index]
                    ),
                    sunrise=daily_data["sunrise"][index],
                    sunset=daily_data["sunset"][index],
                )
            )

        return WeatherData(
            location=location,
            current=current,
            forecast=forecast,
        )