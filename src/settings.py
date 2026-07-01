import json
from pathlib import Path


DEFAULT_SETTINGS = {
    "template_path": "",
    "font_path": "",
    "excel_path": "",
    "output_dir": "",

    "question_color": "#FFFFFF",
    "answer_color": "#FFFFFF",

    "question_outline": "#000000",
    "answer_outline": "#000000",

    "question_outline_enabled": True,
    "answer_outline_enabled": True,

    "question_font_max": 32,
    "question_font_min": 18,

    "answer_font_max": 28,
    "answer_font_min": 20,
}


class SettingsManager:

    def __init__(self, filename):

        self.file = Path(filename)

        self.settings = DEFAULT_SETTINGS.copy()

        self.load()

    def load(self):

        if not self.file.exists():
            return

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            self.settings.update(data)

        except Exception:
            pass

    def save(self):

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.settings,
                f,
                indent=4
            )

    def get(self, key, default=None):

        return self.settings.get(
            key,
            default
        )

    def set(self, key, value):

        self.settings[key] = value

    def reset(self):

        self.settings = DEFAULT_SETTINGS.copy()