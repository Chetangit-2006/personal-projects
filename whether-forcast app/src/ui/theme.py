BACKGROUND = "#0F172A"
SURFACE = "#172033"
SURFACE_LIGHT = "#1E293B"
BORDER = "#334155"

TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#CBD5E1"
TEXT_MUTED = "#94A3B8"

ACCENT = "#38BDF8"
ACCENT_DARK = "#0284C7"

SUCCESS = "#22C55E"
WARNING = "#F59E0B"
ERROR = "#EF4444"

FONT_FAMILY = "Segoe UI"

TITLE_FONT = (FONT_FAMILY, 24, "bold")
SUBTITLE_FONT = (FONT_FAMILY, 11)
HEADING_FONT = (FONT_FAMILY, 16, "bold")
NORMAL_FONT = (FONT_FAMILY, 10)
SMALL_FONT = (FONT_FAMILY, 9)
TEMPERATURE_FONT = (FONT_FAMILY, 42, "bold")
ICON_FONT = (FONT_FAMILY, 42)
FORECAST_ICON_FONT = (FONT_FAMILY, 25)


def configure_styles(style):
    style.theme_use("clam")

    style.configure(
        "App.TFrame",
        background=BACKGROUND,
    )

    style.configure(
        "Card.TFrame",
        background=SURFACE,
    )

    style.configure(
        "TLabel",
        background=BACKGROUND,
        foreground=TEXT_PRIMARY,
        font=NORMAL_FONT,
    )

    style.configure(
        "Card.TLabel",
        background=SURFACE,
        foreground=TEXT_PRIMARY,
        font=NORMAL_FONT,
    )

    style.configure(
        "Title.TLabel",
        background=BACKGROUND,
        foreground=TEXT_PRIMARY,
        font=TITLE_FONT,
    )

    style.configure(
        "Subtitle.TLabel",
        background=BACKGROUND,
        foreground=TEXT_SECONDARY,
        font=SUBTITLE_FONT,
    )

    style.configure(
        "Heading.TLabel",
        background=BACKGROUND,
        foreground=TEXT_PRIMARY,
        font=HEADING_FONT,
    )

    style.configure(
        "CardHeading.TLabel",
        background=SURFACE,
        foreground=TEXT_PRIMARY,
        font=HEADING_FONT,
    )

    style.configure(
        "Muted.TLabel",
        background=SURFACE,
        foreground=TEXT_MUTED,
        font=SMALL_FONT,
    )

    style.configure(
        "Accent.TLabel",
        background=SURFACE,
        foreground=ACCENT,
        font=HEADING_FONT,
    )

    style.configure(
        "Search.TEntry",
        fieldbackground=SURFACE_LIGHT,
        foreground=TEXT_PRIMARY,
        insertcolor=TEXT_PRIMARY,
        borderwidth=0,
        padding=10,
        font=NORMAL_FONT,
    )

    style.configure(
        "Primary.TButton",
        background=ACCENT_DARK,
        foreground=TEXT_PRIMARY,
        borderwidth=0,
        padding=(14, 9),
        font=(FONT_FAMILY, 10, "bold"),
    )

    style.map(
        "Primary.TButton",
        background=[
            ("active", ACCENT),
            ("pressed", ACCENT_DARK),
        ],
    )

    style.configure(
        "Secondary.TButton",
        background=SURFACE_LIGHT,
        foreground=TEXT_PRIMARY,
        borderwidth=0,
        padding=(12, 9),
        font=(FONT_FAMILY, 10),
    )

    style.map(
        "Secondary.TButton",
        background=[
            ("active", BORDER),
            ("pressed", SURFACE),
        ],
    )