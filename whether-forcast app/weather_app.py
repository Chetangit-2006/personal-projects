import tkinter as tk
from tkinter import ttk, messagebox
import requests


# ============================================================
# WEATHER CODE DESCRIPTION
# ============================================================

def get_weather_description(code):
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    return weather_codes.get(code, "Unknown weather")


# ============================================================
# WEATHER ICON
# ============================================================

def get_weather_icon(code, is_day):
    if code == 0:
        return "☀️" if is_day else "🌙"

    if code in [1, 2]:
        return "🌤️" if is_day else "🌙"

    if code == 3:
        return "☁️"

    if code in [45, 48]:
        return "🌫️"

    if code in [51, 53, 55, 56, 57]:
        return "🌦️"

    if code in [61, 63, 65, 66, 67, 80, 81, 82]:
        return "🌧️"

    if code in [71, 73, 75, 77, 85, 86]:
        return "❄️"

    if code in [95, 96, 99]:
        return "⛈️"

    return "🌤️"


# ============================================================
# FIND CITY LOCATION
# ============================================================

def get_location(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if "results" not in data:
        return None

    result = data["results"][0]

    return {
        "name": result["name"],
        "country": result.get("country", "Unknown"),
        "latitude": result["latitude"],
        "longitude": result["longitude"]
    }


# ============================================================
# GET WEATHER
# ============================================================

def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "is_day,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# MAIN APPLICATION
# ============================================================

class WeatherApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Weather App")
        self.root.geometry("850x700")
        self.root.minsize(750, 620)

        self.root.configure(bg="#0F172A")

        # ----------------------------------------------------
        # COLORS
        # ----------------------------------------------------

        self.bg = "#0F172A"
        self.card = "#1E293B"
        self.card_light = "#334155"
        self.text = "#F8FAFC"
        self.text_secondary = "#94A3B8"
        self.accent = "#38BDF8"
        self.accent_hover = "#0EA5E9"
        self.success = "#22C55E"
        self.error = "#EF4444"

        self.setup_styles()
        self.create_interface()

        # Load initial example
        self.city_entry.insert(0, "Nashik")

    # ========================================================
    # STYLES
    # ========================================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Search.TEntry",
            fieldbackground=self.card_light,
            foreground=self.text,
            borderwidth=0,
            padding=12,
            font=("Segoe UI", 12)
        )

        style.configure(
            "Search.TButton",
            background=self.accent,
            foreground="#FFFFFF",
            borderwidth=0,
            padding=(20, 12),
            font=("Segoe UI Semibold", 11)
        )

        style.map(
            "Search.TButton",
            background=[
                ("active", self.accent_hover)
            ]
        )

    # ========================================================
    # CREATE INTERFACE
    # ========================================================

    def create_interface(self):

        # Main container
        main = tk.Frame(
            self.root,
            bg=self.bg
        )

        main.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=30
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            main,
            bg=self.bg
        )

        header.pack(
            fill="x",
            pady=(0, 25)
        )

        title_frame = tk.Frame(
            header,
            bg=self.bg
        )

        title_frame.pack(side="left")

        title = tk.Label(
            title_frame,
            text="🌤  WEATHER APP",
            bg=self.bg,
            fg=self.text,
            font=("Segoe UI", 25, "bold")
        )

        title.pack(anchor="w")

        subtitle = tk.Label(
            title_frame,
            text="Real-time weather information",
            bg=self.bg,
            fg=self.text_secondary,
            font=("Segoe UI", 11)
        )

        subtitle.pack(
            anchor="w",
            pady=(3, 0)
        )

        # Online status
        status_frame = tk.Frame(
            header,
            bg=self.bg
        )

        status_frame.pack(
            side="right",
            pady=8
        )

        status_dot = tk.Label(
            status_frame,
            text="●",
            bg=self.bg,
            fg=self.success,
            font=("Segoe UI", 13)
        )

        status_dot.pack(side="left")

        status_text = tk.Label(
            status_frame,
            text=" ONLINE",
            bg=self.bg,
            fg=self.text_secondary,
            font=("Segoe UI", 10)
        )

        status_text.pack(side="left")

        # ----------------------------------------------------
        # SEARCH AREA
        # ----------------------------------------------------

        search_card = tk.Frame(
            main,
            bg=self.card
        )

        search_card.pack(
            fill="x",
            pady=(0, 25)
        )

        search_card.columnconfigure(0, weight=1)

        search_inner = tk.Frame(
            search_card,
            bg=self.card
        )

        search_inner.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=15,
            pady=15
        )

        search_inner.columnconfigure(0, weight=1)

        self.city_entry = ttk.Entry(
            search_inner,
            style="Search.TEntry"
        )

        self.city_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        self.city_entry.bind(
            "<Return>",
            lambda event: self.search_weather()
        )

        search_button = ttk.Button(
            search_inner,
            text="SEARCH",
            style="Search.TButton",
            command=self.search_weather
        )

        search_button.grid(
            row=0,
            column=1
        )

        # ----------------------------------------------------
        # LOCATION
        # ----------------------------------------------------

        self.location_label = tk.Label(
            main,
            text="Search for a city",
            bg=self.bg,
            fg=self.text,
            font=("Segoe UI", 21, "bold")
        )

        self.location_label.pack(
            pady=(5, 2)
        )

        self.condition_label = tk.Label(
            main,
            text="Enter a city above to get current weather",
            bg=self.bg,
            fg=self.text_secondary,
            font=("Segoe UI", 11)
        )

        self.condition_label.pack()

        # ----------------------------------------------------
        # MAIN WEATHER
        # ----------------------------------------------------

        weather_main = tk.Frame(
            main,
            bg=self.bg
        )

        weather_main.pack(
            pady=20
        )

        self.weather_icon = tk.Label(
            weather_main,
            text="🌤️",
            bg=self.bg,
            fg=self.text,
            font=("Segoe UI Emoji", 65)
        )

        self.weather_icon.pack()

        self.temperature_label = tk.Label(
            weather_main,
            text="--°C",
            bg=self.bg,
            fg=self.text,
            font=("Segoe UI", 48, "bold")
        )

        self.temperature_label.pack()

        self.feels_label = tk.Label(
            weather_main,
            text="Feels like --°C",
            bg=self.bg,
            fg=self.text_secondary,
            font=("Segoe UI", 12)
        )

        self.feels_label.pack()

        # ----------------------------------------------------
        # WEATHER CARDS
        # ----------------------------------------------------

        cards_frame = tk.Frame(
            main,
            bg=self.bg
        )

        cards_frame.pack(
            fill="x",
            pady=(10, 20)
        )

        for i in range(3):
            cards_frame.columnconfigure(
                i,
                weight=1
            )

        # Humidity
        self.humidity_card = self.create_weather_card(
            cards_frame,
            0,
            "💧",
            "HUMIDITY",
            "--%"
        )

        # Wind
        self.wind_card = self.create_weather_card(
            cards_frame,
            1,
            "💨",
            "WIND SPEED",
            "-- km/h"
        )

        # Day / Night
        self.day_card = self.create_weather_card(
            cards_frame,
            2,
            "☀️",
            "TIME STATUS",
            "--"
        )

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        footer = tk.Frame(
            main,
            bg=self.bg
        )

        footer.pack(
            fill="x",
            side="bottom"
        )

        self.updated_label = tk.Label(
            footer,
            text="",
            bg=self.bg,
            fg=self.text_secondary,
            font=("Segoe UI", 9)
        )

        self.updated_label.pack(
            side="left"
        )

        provider = tk.Label(
            footer,
            text="Weather data provided by Open-Meteo",
            bg=self.bg,
            fg=self.text_secondary,
            font=("Segoe UI", 9)
        )

        provider.pack(
            side="right"
        )

    # ========================================================
    # CREATE WEATHER CARD
    # ========================================================

    def create_weather_card(
        self,
        parent,
        column,
        icon,
        title,
        value
    ):

        card = tk.Frame(
            parent,
            bg=self.card,
            height=120
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=6
        )

        card.pack_propagate(False)

        icon_label = tk.Label(
            card,
            text=icon,
            bg=self.card,
            fg=self.text,
            font=("Segoe UI Emoji", 22)
        )

        icon_label.pack(
            pady=(12, 2)
        )

        title_label = tk.Label(
            card,
            text=title,
            bg=self.card,
            fg=self.text_secondary,
            font=("Segoe UI", 8, "bold")
        )

        title_label.pack()

        value_label = tk.Label(
            card,
            text=value,
            bg=self.card,
            fg=self.text,
            font=("Segoe UI", 13, "bold")
        )

        value_label.pack(
            pady=(4, 0)
        )

        return value_label

    # ========================================================
    # SEARCH WEATHER
    # ========================================================

    def search_weather(self):

        city = self.city_entry.get().strip()

        if not city:

            messagebox.showwarning(
                "Missing City",
                "Please enter a city name."
            )

            return

        # Loading state
        self.condition_label.config(
            text="Searching for city...",
            fg=self.accent
        )

        self.root.update_idletasks()

        try:

            # Find location
            location = get_location(city)

            if location is None:

                self.condition_label.config(
                    text="City not found. Please check the spelling.",
                    fg=self.error
                )

                messagebox.showerror(
                    "City Not Found",
                    f"Could not find '{city}'.\n\n"
                    "Please check the city name and try again."
                )

                return

            self.condition_label.config(
                text="Fetching latest weather information...",
                fg=self.accent
            )

            self.root.update_idletasks()

            # Get weather
            data = get_weather(
                location["latitude"],
                location["longitude"]
            )

            # Display
            self.display_weather(
                location,
                data
            )

        except requests.exceptions.Timeout:

            self.show_error(
                "The request timed out.\n\n"
                "Please check your internet connection."
            )

        except requests.exceptions.ConnectionError:

            self.show_error(
                "Unable to connect to the weather service.\n\n"
                "Please check your internet connection."
            )

        except requests.exceptions.HTTPError as error:

            self.show_error(
                f"Weather API error:\n\n{error}"
            )

        except Exception as error:

            self.show_error(
                f"Something went wrong:\n\n{error}"
            )

    # ========================================================
    # DISPLAY WEATHER
    # ========================================================

    def display_weather(
        self,
        location,
        data
    ):

        current = data["current"]

        temperature = current["temperature_2m"]

        humidity = current[
            "relative_humidity_2m"
        ]

        feels_like = current[
            "apparent_temperature"
        ]

        wind_speed = current[
            "wind_speed_10m"
        ]

        weather_code = current[
            "weather_code"
        ]

        is_day = current[
            "is_day"
        ]

        time = current[
            "time"
        ]

        condition = get_weather_description(
            weather_code
        )

        icon = get_weather_icon(
            weather_code,
            is_day
        )

        # Location
        self.location_label.config(
            text=f"{location['name']}, {location['country']}",
            fg=self.text
        )

        # Condition
        self.condition_label.config(
            text=condition,
            fg=self.text_secondary
        )

        # Icon
        self.weather_icon.config(
            text=icon
        )

        # Temperature
        self.temperature_label.config(
            text=f"{temperature}°C"
        )

        # Feels like
        self.feels_label.config(
            text=f"Feels like {feels_like}°C"
        )

        # Cards
        self.humidity_card.config(
            text=f"{humidity}%"
        )

        self.wind_card.config(
            text=f"{wind_speed} km/h"
        )

        if is_day == 1:

            self.day_card.config(
                text="Day"
            )

        else:

            self.day_card.config(
                text="Night"
            )

        # Footer
        formatted_time = time.replace(
            "T",
            " "
        )

        self.updated_label.config(
            text=f"Updated: {formatted_time}"
        )

        # Window title
        self.root.title(
            f"Weather App - {location['name']}"
        )

    # ========================================================
    # ERROR DISPLAY
    # ========================================================

    def show_error(self, message):

        self.condition_label.config(
            text="Unable to retrieve weather data",
            fg=self.error
        )

        messagebox.showerror(
            "Weather App Error",
            message
        )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

def main():

    root = tk.Tk()

    app = WeatherApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()