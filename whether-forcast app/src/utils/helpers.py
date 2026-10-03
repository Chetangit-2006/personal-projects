from datetime import datetime


def celsius_to_fahrenheit(value: float) -> float:
    return (value * 9 / 5) + 32


def format_temperature(value: float, unit: str = "C") -> str:
    if unit == "F":
        value = celsius_to_fahrenheit(value)

    return f"{value:.1f}°{unit}"


def format_date(date_string: str) -> str:
    try:
        date = datetime.strptime(date_string, "%Y-%m-%d")
        return date.strftime("%a")
    except ValueError:
        return date_string


def format_date_long(date_string: str) -> str:
    try:
        date = datetime.strptime(date_string, "%Y-%m-%d")
        return date.strftime("%d %b %Y")
    except ValueError:
        return date_string


def format_time(time_string: str) -> str:
    try:
        time_string = time_string.replace("Z", "")
        date = datetime.fromisoformat(time_string)
        return date.strftime("%I:%M %p")
    except ValueError:
        return time_string


def format_local_datetime(datetime_string: str) -> str:
    try:
        date = datetime.fromisoformat(datetime_string)
        return date.strftime("%d %b %Y, %I:%M %p")
    except ValueError:
        return datetime_string