import unittest

from src.api.weather_api import WeatherAPI
from src.models.weather_model import Location
from src.utils.weather_codes import (
    get_weather_description,
    get_weather_icon,
)


class TestWeatherCodes(unittest.TestCase):

    def test_clear_sky_description(self):
        self.assertEqual(
            get_weather_description(0),
            "Clear sky",
        )

    def test_clear_sky_icon(self):
        self.assertEqual(
            get_weather_icon(0),
            "☀",
        )


class TestWeatherAPI(unittest.TestCase):

    def test_location_creation(self):
        location = Location(
            name="Nashik",
            country="India",
            latitude=20.0,
            longitude=73.0,
            timezone="Asia/Kolkata",
        )

        self.assertEqual(location.name, "Nashik")
        self.assertEqual(location.country, "India")


if __name__ == "__main__":
    unittest.main()