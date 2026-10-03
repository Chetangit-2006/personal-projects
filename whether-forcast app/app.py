import tkinter as tk

from src.ui.main_window import WeatherApp


def main():
    root = tk.Tk()
    WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()