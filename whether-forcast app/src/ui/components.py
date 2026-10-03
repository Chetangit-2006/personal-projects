import tkinter as tk
from tkinter import ttk

from src.ui.theme import (
    ACCENT,
    BORDER,
    SURFACE,
    SURFACE_LIGHT,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


class MetricCard(ttk.Frame):
    def __init__(
        self,
        parent,
        title: str,
        value: str,
        icon: str,
    ):
        super().__init__(
            parent,
            style="Card.TFrame",
            padding=15,
        )

        self.columnconfigure(1, weight=1)

        icon_label = ttk.Label(
            self,
            text=icon,
            style="Accent.TLabel",
            font=("Segoe UI", 20),
        )
        icon_label.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(0, 12),
        )

        ttk.Label(
            self,
            text=title,
            style="Muted.TLabel",
        ).grid(
            row=0,
            column=1,
            sticky="w",
        )

        self.value_label = ttk.Label(
            self,
            text=value,
            style="Card.TLabel",
            font=("Segoe UI", 13, "bold"),
        )
        self.value_label.grid(
            row=1,
            column=1,
            sticky="w",
            pady=(3, 0),
        )

    def update_value(self, value: str):
        self.value_label.configure(text=value)


class ForecastCard(tk.Frame):
    def __init__(
        self,
        parent,
        day: str,
        date: str,
        icon: str,
        condition: str,
        high: str,
        low: str,
        rain_probability: str,
    ):
        super().__init__(
            parent,
            bg=SURFACE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=14,
            pady=14,
        )

        tk.Label(
            self,
            text=day,
            bg=SURFACE,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 11, "bold"),
        ).pack()

        tk.Label(
            self,
            text=date,
            bg=SURFACE,
            fg=TEXT_MUTED,
            font=("Segoe UI", 8),
        ).pack(pady=(2, 8))

        tk.Label(
            self,
            text=icon,
            bg=SURFACE,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 25),
        ).pack(pady=3)

        tk.Label(
            self,
            text=condition,
            bg=SURFACE,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 9),
            wraplength=100,
        ).pack(pady=(4, 8))

        tk.Label(
            self,
            text=f"{high}  /  {low}",
            bg=SURFACE,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
        ).pack()

        tk.Label(
            self,
            text=f"💧 {rain_probability}",
            bg=SURFACE,
            fg=ACCENT,
            font=("Segoe UI", 9),
        ).pack(pady=(8, 0))