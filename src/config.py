import json
from pathlib import Path


class Config:
    """
    Central configuration object for card generator.

    Holds:
        - box layout (question/answer regions)
        - style settings (fonts, colors, stroke)
        - output settings
    """

    def __init__(self, data: dict):
        self._data = data

        # Core sections
        self.boxes = data.get("boxes", {})
        self.style = data.get("style", {})
        self.output = data.get("output", {})

        # Ensure required structure exists
        self.style.setdefault("question", {})
        self.style.setdefault("answer", {})

    # -------------------------------------------------
    # BOXES
    # -------------------------------------------------

    def get_box(self, name: str):
        if name not in self.boxes:
            raise KeyError(f"Missing box in config: {name}")
        return self.boxes[name]

    # -------------------------------------------------
    # STYLE ACCESS
    # -------------------------------------------------

    def get_style(self, section: str):
        return self.style.get(section, {})

    def set_style(self, section: str, key: str, value):
        if section not in self.style:
            self.style[section] = {}

        self.style[section][key] = value

    def safe_style(self, section: str):
        """
        Always returns a safe mutable dict.
        """
        return self.style.setdefault(section, {})

    # -------------------------------------------------
    # OUTPUT SETTINGS
    # -------------------------------------------------

    def get_output(self):
        return self.output

    # -------------------------------------------------
    # FONT (MS WORD STYLE SUPPORT)
    # -------------------------------------------------

    def get_font_family(self):
        """
        Optional centralized font storage (Word-style).
        """
        return self._data.get("font_family", "Arial")

    def set_font_family(self, font_name: str):
        self._data["font_family"] = font_name

    # -------------------------------------------------
    # SAVE CONFIG
    # -------------------------------------------------

    def save(self, config_path):
        config_path = Path(config_path)

        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=4, ensure_ascii=False)


# =========================================================
# LOAD CONFIG
# =========================================================

def load_config(config_path):
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------

    if "boxes" not in data:
        raise KeyError("'boxes' section is missing in config.json")

    if "style" not in data:
        data["style"] = {}

    if "output" not in data:
        data["output"] = {}

    # Required boxes
    required_boxes = ["question", "answer"]

    for box in required_boxes:
        if box not in data["boxes"]:
            raise KeyError(f"Missing required box: {box}")

    # Ensure structure consistency
    data["style"].setdefault("question", {})
    data["style"].setdefault("answer", {})

    return Config(data)