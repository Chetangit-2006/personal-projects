import threading
import tkinter as tk
from tkinter import messagebox, ttk

from src.api.weather_api import WeatherAPI, WeatherAPIError
from src.ui.components import ForecastCard, MetricCard
from src.ui.theme import (
    ACCENT,
    BACKGROUND,
    BORDER,
    ERROR,
    FONT_FAMILY,
    FORECAST_ICON_FONT,
    HEADING_FONT,
    ICON_FONT,
    SURFACE,
    SURFACE_LIGHT,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEMPERATURE_FONT,
    configure_styles,
)
from src.utils.helpers import (
    format_date,
    format_date_long,
    format_local_datetime,
    format_temperature,
    format_time,
)
from src.utils.weather_codes import (
    get_weather_description,
    get_weather_icon,
)


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("1100x760")
        self.root.minsize(900, 650)
        self.root.configure(bg=BACKGROUND)

        self.api = WeatherAPI()
        self.current_weather_data = None
        self.current_city = ""
        self.unit = "C"

        self.style = ttk.Style()
        configure_styles(self.style)

        self.build_ui()

        self.search_var.set("Nashik")
        self.search_weather()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def build_ui(self):
        self.main_container = ttk.Frame(
            self.root,
            style="App.TFrame",
            padding=20,
        )
        self.main_container.pack(
            fill="both",
            expand=True,
        )

        self.build_header()
        self.build_search_bar()
        self.build_status()

        self.content = ttk.Frame(
            self.main_container,
            style="App.TFrame",
        )
        self.content.pack(
            fill="both",
            expand=True,
            pady=(15, 0),
        )

        self.build_current_section()
        self.build_forecast_section()

    def build_header(self):
        header = ttk.Frame(
            self.main_container,
            style="App.TFrame",
        )
        header.pack(
            fill="x",
            pady=(0, 15),
        )

        title_frame = ttk.Frame(
            header,
            style="App.TFrame",
        )
        title_frame.pack(
            side="left",
            fill="x",
            expand=True,
        )

        ttk.Label(
            title_frame,
            text="Weather App",
            style="Title.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            title_frame,
            text="Real-time weather and 7-day forecast",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(3, 0))

        self.unit_button = ttk.Button(
            header,
            text="°C  |  °F",
            style="Secondary.TButton",
            command=self.toggle_unit,
        )
        self.unit_button.pack(side="right")

    def build_search_bar(self):
        search_frame = ttk.Frame(
            self.main_container,
            style="App.TFrame",
        )
        search_frame.pack(
            fill="x",
            pady=(0, 5),
        )

        entry_container = tk.Frame(
            search_frame,
            bg=SURFACE_LIGHT,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        entry_container.pack(
            side="left",
            fill="x",
            expand=True,
        )

        tk.Label(
            entry_container,
            text="🔍",
            bg=SURFACE_LIGHT,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 12),
        ).pack(
            side="left",
            padx=(12, 5),
        )

        self.search_var = tk.StringVar()

        self.search_entry = ttk.Entry(
            entry_container,
            textvariable=self.search_var,
            style="Search.TEntry",
        )
        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_weather(),
        )

        self.search_button = ttk.Button(
            search_frame,
            text="Search",
            style="Primary.TButton",
            command=self.search_weather,
        )
        self.search_button.pack(
            side="left",
            padx=(10, 0),
        )

        self.refresh_button = ttk.Button(
            search_frame,
            text="↻ Refresh",
            style="Secondary.TButton",
            command=self.refresh_weather,
        )
        self.refresh_button.pack(
            side="left",
            padx=(8, 0),
        )

    def build_status(self):
        self.status_var = tk.StringVar(
            value="Ready"
        )

        self.status_label = ttk.Label(
            self.main_container,
            textvariable=self.status_var,
            style="Subtitle.TLabel",
        )
        self.status_label.pack(
            anchor="w",
            pady=(2, 0),
        )

    def build_current_section(self):
        current_container = tk.Frame(
            self.content,
            bg=SURFACE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=20,
            pady=20,
        )
        current_container.pack(
            fill="x",
            pady=(0, 15),
        )

        current_container.columnconfigure(
            0,
            weight=2,
        )
        current_container.columnconfigure(
            1,
            weight=1,
        )

        # Left section
        self.current_left = tk.Frame(
            current_container,
            bg=SURFACE,
        )
        self.current_left.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.location_label = tk.Label(
            self.current_left,
            text="Loading...",
            bg=SURFACE,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 20, "bold"),
        )
        self.location_label.pack(
            anchor="w"
        )

        self.local_time_label = tk.Label(
            self.current_left,
            text="",
            bg=SURFACE,
            fg=TEXT_MUTED,
            font=("Segoe UI", 9),
        )
        self.local_time_label.pack(
            anchor="w",
            pady=(3, 12),
        )

        weather_main = tk.Frame(
            self.current_left,
            bg=SURFACE,
        )
        weather_main.pack(
            anchor="w",
        )

        self.weather_icon_label = tk.Label(
            weather_main,
            text="☀",
            bg=SURFACE,
            fg=TEXT_PRIMARY,
            font=ICON_FONT,
        )
        self.weather_icon_label.pack(
            side="left",
            padx=(0, 15),
        )

        temperature_frame = tk.Frame(
            weather_main,
            bg=SURFACE,
        )
        temperature_frame.pack(
            side="left"
        )

        self.temperature_label = tk.Label(
            temperature_frame,
            text="--",
            bg=SURFACE,
            fg=TEXT_PRIMARY,
            font=TEMPERATURE_FONT,
        )
        self.temperature_label.pack(
            anchor="w"
        )

        self.condition_label = tk.Label(
            temperature_frame,
            text="Loading...",
            bg=SURFACE,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 12),
        )
        self.condition_label.pack(
            anchor="w"
        )

        self.day_status_label = tk.Label(
            temperature_frame,
            text="",
            bg=SURFACE,
            fg=ACCENT,
            font=("Segoe UI", 9, "bold"),
        )
        self.day_status_label.pack(
            anchor="w",
            pady=(3, 0),
        )

        # Right section
        self.current_right = tk.Frame(
            current_container,
            bg=SURFACE,
        )
        self.current_right.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(30, 0),
        )

        self.feels_card = MetricCard(
            self.current_right,
            "Feels Like",
            "--",
            "🌡",
        )
        self.feels_card.pack(
            fill="x",
            pady=(0, 8),
        )

        self.humidity_card = MetricCard(
            self.current_right,
            "Humidity",
            "--",
            "💧",
        )
        self.humidity_card.pack(
            fill="x",
            pady=8,
        )

        self.wind_card = MetricCard(
            self.current_right,
            "Wind Speed",
            "--",
            "💨",
        )
        self.wind_card.pack(
            fill="x",
            pady=8,
        )

        self.sun_card = MetricCard(
            self.current_right,
            "Sunrise / Sunset",
            "--",
            "🌅",
        )
        self.sun_card.pack(
            fill="x",
            pady=(8, 0),
        )

    def build_forecast_section(self):
        ttk.Label(
            self.content,
            text="7-Day Forecast",
            style="Heading.TLabel",
        ).pack(
            anchor="w",
            pady=(0, 8),
        )

        self.forecast_container = tk.Frame(
            self.content,
            bg=BACKGROUND,
        )
        self.forecast_container.pack(
            fill="x",
        )

        for index in range(7):
            self.forecast_container.columnconfigure(
                index,
                weight=1,
            )

        self.forecast_cards = []

    # ---------------------------------------------------------
    # WEATHER SEARCH
    # ---------------------------------------------------------

    def search_weather(self):
        city = self.search_var.get().strip()

        if not city:
            messagebox.showwarning(
                "Missing City",
                "Please enter a city name.",
            )
            return

        self.set_loading(True)

        thread = threading.Thread(
            target=self.fetch_weather,
            args=(city,),
            daemon=True,
        )
        thread.start()

    def refresh_weather(self):
        if self.current_city:
            self.search_var.set(self.current_city)
            self.search_weather()
        else:
            self.search_weather()

    def fetch_weather(self, city):
        try:
            weather_data = self.api.get_weather(city)

            self.root.after(
                0,
                lambda: self.display_weather(weather_data),
            )

        except WeatherAPIError as exc:
            self.root.after(
                0,
                lambda: self.show_error(str(exc)),
            )

        except Exception as exc:
            self.root.after(
                0,
                lambda: self.show_error(
                    f"Unexpected error: {exc}"
                ),
            )

    # ---------------------------------------------------------
    # DISPLAY
    # ---------------------------------------------------------

    def display_weather(self, weather_data):
        self.current_weather_data = weather_data
        self.current_city = weather_data.location.name

        location = weather_data.location
        current = weather_data.current

        description = get_weather_description(
            current.weather_code
        )
        icon = get_weather_icon(
            current.weather_code
        )

        self.location_label.configure(
            text=f"{location.name}, {location.country}"
        )

        self.local_time_label.configure(
            text=(
                f"Local time: "
                f"{format_local_datetime(current.local_time)}"
            )
        )

        self.weather_icon_label.configure(
            text=icon
        )

        self.temperature_label.configure(
            text=format_temperature(
                current.temperature,
                self.unit,
            )
        )

        self.condition_label.configure(
            text=description
        )

        self.day_status_label.configure(
            text="Daytime" if current.is_day else "Nighttime"
        )

        self.feels_card.update_value(
            format_temperature(
                current.feels_like,
                self.unit,
            )
        )

        self.humidity_card.update_value(
            f"{current.humidity}%"
        )

        self.wind_card.update_value(
            f"{current.wind_speed:.1f} km/h"
        )

        if weather_data.forecast:
            first_day = weather_data.forecast[0]

            sunrise = format_time(
                first_day.sunrise
            )
            sunset = format_time(
                first_day.sunset
            )

            self.sun_card.update_value(
                f"{sunrise} / {sunset}"
            )

        self.update_forecast(
            weather_data.forecast
        )

        self.status_var.set(
            "Weather updated successfully"
        )

        self.set_loading(False)

    def update_forecast(self, forecast):
        for card in self.forecast_cards:
            card.destroy()

        self.forecast_cards.clear()

        for index, day in enumerate(forecast[:7]):
            card = ForecastCard(
                self.forecast_container,
                day=format_date(day.date),
                date=format_date_long(day.date),
                icon=get_weather_icon(day.weather_code),
                condition=get_weather_description(
                    day.weather_code
                ),
                high=format_temperature(
                    day.temperature_max,
                    self.unit,
                ),
                low=format_temperature(
                    day.temperature_min,
                    self.unit,
                ),
                rain_probability=(
                    f"{day.precipitation_probability}%"
                ),
            )

            card.grid(
                row=0,
                column=index,
                sticky="nsew",
                padx=4,
            )

            self.forecast_cards.append(card)

    # ---------------------------------------------------------
    # UNIT SWITCHING
    # ---------------------------------------------------------

    def toggle_unit(self):
        self.unit = "F" if self.unit == "C" else "C"

        if self.current_weather_data:
            self.display_weather(
                self.current_weather_data
            )

    # ---------------------------------------------------------
    # STATE / ERRORS
    # ---------------------------------------------------------

    def set_loading(self, loading: bool):
        if loading:
            self.status_var.set(
                "Loading weather data..."
            )

            self.search_button.configure(
                state="disabled"
            )

            self.refresh_button.configure(
                state="disabled"
            )

        else:
            self.search_button.configure(
                state="normal"
            )

            self.refresh_button.configure(
                state="normal"
            )

    def show_error(self, message):
        self.set_loading(False)

        self.status_var.set(
            "Unable to update weather"
        )

        messagebox.showerror(
            "Weather App Error",
            message,
        )