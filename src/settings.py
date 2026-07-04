import json
from pathlib import Path
from copy import deepcopy


# =========================================================
# DEFAULT SETTINGS (UI STATE, NOT RENDER CONFIG)
# =========================================================
DEFAULT_SETTINGS = {
    # ---------------- FILE PATHS ----------------
    "template_path": "",
    "font_path": "",
    "excel_path": "",
    "output_dir": "",

    # ---------------- COLORS ----------------
    "question_color": "#FFFFFF",
    "answer_color": "#FFFFFF",

    "question_outline": "#000000",
    "answer_outline": "#000000",

    "question_outline_enabled": True,
    "answer_outline_enabled": True,

    # ---------------- FONT SIZES ----------------
    "question_font_max": 32,
    "question_font_min": 18,

    "answer_font_max": 28,
    "answer_font_min": 20,

    # ---------------- LAYOUT ----------------
    "question_offset_y": 0,
    "answer_offset_y": 0,

    # ---------------- UI STATE ----------------
    "window_width": 1200,
    "window_height": 800,

    "last_font": "Arial",

    # ---------------- RUNTIME FLAGS ----------------
    "auto_preview": True,
}


# =========================================================
# SETTINGS MANAGER
# =========================================================
class SettingsManager:
    """
    Handles persistent UI state.

    IMPORTANT:
    - This is NOT rendering config (that's config.py)
    - This is UI memory (last used values, paths, preferences)
    """

    def __init__(self, filename):
        self.file = Path(filename)
        self.settings = deepcopy(DEFAULT_SETTINGS)
        self.load()

    # =====================================================
    # LOAD SETTINGS
    # =====================================================
    def load(self):
        if not self.file.exists():
            return

        try:
            with open(self.file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                self.settings.update(data)

        except Exception:
            # fail silently (UI should never crash)
            pass

    # =====================================================
    # SAVE SETTINGS
    # =====================================================
    def save(self):
        self.file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)

    # =====================================================
    # GET VALUE
    # =====================================================
    def get(self, key, default=None):
        return self.settings.get(key, default)

    # =====================================================
    # SET VALUE
    # =====================================================
    def set(self, key, value):
        self.settings[key] = value

    # =====================================================
    # BULK UPDATE (VERY USEFUL FOR GUI)
    # =====================================================
    def update(self, data: dict):
        if isinstance(data, dict):
            self.settings.update(data)

    # =====================================================
    # RESET SETTINGS
    # =====================================================
    def reset(self):
        self.settings = deepcopy(DEFAULT_SETTINGS)

    # =====================================================
    # PATH HELPERS (COMMON UI NEED)
    # =====================================================
    def set_paths(self, template=None, excel=None, output=None, font=None):
        if template is not None:
            self.settings["template_path"] = str(template)

        if excel is not None:
            self.settings["excel_path"] = str(excel)

        if output is not None:
            self.settings["output_dir"] = str(output)

        if font is not None:
            self.settings["font_path"] = str(font)

    # =====================================================
    # WINDOW STATE (FOR NEXT LAUNCH)
    # =====================================================
    def set_window_size(self, width, height):
        self.settings["window_width"] = width
        self.settings["window_height"] = height

    def get_window_size(self):
        return (
            self.settings.get("window_width", 1200),
            self.settings.get("window_height", 800),
        )

    # =====================================================
    # UI PREFERENCES HELPERS
    # =====================================================
    def toggle(self, key):
        """
        Toggle boolean settings (used for checkboxes).
        """
        if key in self.settings:
            self.settings[key] = not self.settings[key]

    def is_enabled(self, key):
        return bool(self.settings.get(key, False))