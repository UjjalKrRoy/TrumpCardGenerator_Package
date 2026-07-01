"""
UI STYLE SYSTEM

Purpose:
- Centralize all colors, spacing, and font rules
- Ensure consistent UI appearance across the app
- Enable future theme switching (light/dark modes)
"""


# =========================================================
# COLOR SYSTEM
# =========================================================
class Colors:
    """
    Core color palette.
    You can later extend this for dark/light themes.
    """

    # Primary accents
    PRIMARY = "#2D7DFF"
    PRIMARY_DARK = "#1F5FCC"

    # Backgrounds
    BACKGROUND = "#F5F6FA"
    PANEL_BG = "#FFFFFF"

    # Text
    TEXT = "#222222"
    TEXT_MUTED = "#666666"

    # Borders / separators
    BORDER = "#DADDE3"

    # Status
    SUCCESS = "#2ECC71"
    WARNING = "#F1C40F"
    ERROR = "#E74C3C"


# =========================================================
# TYPOGRAPHY SYSTEM
# =========================================================
class Fonts:
    """
    Central font definitions for UI consistency.
    """

    TITLE = ("Arial", 14, "bold")
    SUBTITLE = ("Arial", 11, "bold")
    BODY = ("Arial", 10)
    SMALL = ("Arial", 9)


# =========================================================
# SPACING SYSTEM
# =========================================================
class Spacing:
    """
    Standard spacing units for consistent layout.
    """

    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 24


# =========================================================
# BUTTON STYLE HELPERS
# =========================================================
class ButtonStyle:
    """
    Logical grouping for button behavior styles.
    """

    PRIMARY = {
        "bg": Colors.PRIMARY,
        "fg": "white",
        "activebackground": Colors.PRIMARY_DARK,
        "relief": "flat",
        "padx": 10,
        "pady": 6,
    }

    SECONDARY = {
        "bg": Colors.PANEL_BG,
        "fg": Colors.TEXT,
        "relief": "flat",
        "padx": 10,
        "pady": 6,
    }

    DANGER = {
        "bg": Colors.ERROR,
        "fg": "white",
        "relief": "flat",
        "padx": 10,
        "pady": 6,
    }


# =========================================================
# UI THEME CONTEXT (FUTURE READY)
# =========================================================
class Theme:
    """
    High-level theme configuration.
    Future: can switch between LIGHT / DARK modes.
    """

    name = "light"

    colors = Colors
    fonts = Fonts
    spacing = Spacing

    @classmethod
    def set_theme(cls, theme_name: str):
        """
        Placeholder for future theme switching system.
        """
        cls.name = theme_name

        # Future expansion:
        # if theme_name == "dark":
        #     swap color palette here