# 🌤️ Python Weather App

A professional desktop weather application built with Python and Tkinter using the Open-Meteo API.

## Features

- 🔍 Search weather by city
- 🌡️ Current temperature
- 🤒 Feels-like temperature
- 💧 Humidity
- 💨 Wind speed
- 🌅 Sunrise and sunset
- ☀️ Day/night detection
- 🌦️ Dynamic weather conditions
- 📅 7-day forecast
- 🌧️ Precipitation probability
- 🔄 Refresh weather
- 🌡️ Celsius/Fahrenheit conversion
- ⏳ Loading state
- ❌ Error handling
- 🧩 Modular project architecture
- 🧪 Unit tests
- 🐙 GitHub-ready structure

## Tech Stack

- Python
- Tkinter
- Requests
- Open-Meteo API
- Dataclasses
- Unit Testing

## Project Structure

```text
Python-Weather-App/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── api/
│   │   └── weather_api.py
│   │
│   ├── models/
│   │   └── weather_model.py
│   │
│   ├── ui/
│   │   ├── components.py
│   │   ├── main_window.py
│   │   └── theme.py
│   │
│   └── utils/
│       ├── helpers.py
│       └── weather_codes.py
│
├── assets/
│   ├── icons/
│   └── screenshots/
│
└── tests/
    └── test_weather_api.py