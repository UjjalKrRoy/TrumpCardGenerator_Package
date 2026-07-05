import json
from pathlib import Path
from copy import deepcopy


# =========================================================
# CONFIG CLASS
# =========================================================
class Config:
    """
    Central configuration object.

    Stores:
    - Box positions
    - Typography
    - Colours
    - Output settings
    """

    def __init__(self, data: dict):
        self._data = data

        self.boxes = data.get("boxes", {})
        self.style = data.get("style", {})
        self.output = data.get("output", {})

        # Ensure every style exists
        for section in (
            "question",
            "answer",
            "subject",
            "stage",
        ):
            self.style.setdefault(section, {})

    # =====================================================
    # BOXES
    # =====================================================

    def get_box(self, name):
        if name not in self.boxes:
            raise KeyError(f"Missing box: {name}")
        return self.boxes[name]

    def set_box(self, name, value):
        self.boxes[name] = value

    def update_box_offset(self, name, offset_y):

        if name not in self.boxes:
            raise KeyError(f"Missing box: {name}")

        x, y, w, h = self.boxes[name]

        self.boxes[name] = [
            x,
            y + offset_y,
            w,
            h,
        ]

    def reset_boxes(self, original_boxes):
        self.boxes = deepcopy(original_boxes)

    # =====================================================
    # STYLE
    # =====================================================

    def get_style(self, section):
        return self.style.get(section, {})

    def set_style(self, section, key, value):

        self.style.setdefault(section, {})

        self.style[section][key] = value

    def update_style(self, section, updates):

        self.style.setdefault(section, {})

        self.style[section].update(updates)

    def safe_style(self, section):
        return self.style.setdefault(section, {})

    # =====================================================
    # OUTPUT
    # =====================================================

    def get_output(self):
        return self.output

    def set_output(self, key, value):
        self.output[key] = value

    # =====================================================
    # FONT
    # =====================================================

    def get_font_family(self):
        return self._data.get("font_family", "Arial")

    def set_font_family(self, font):
        self._data["font_family"] = font

    # =====================================================
    # COPY
    # =====================================================

    def copy(self):
        return Config(
            deepcopy(self._data)
        )

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, config_path):

        config_path = Path(config_path)

        config_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            config_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self._data,
                f,
                indent=4,
                ensure_ascii=False,
            )


# =========================================================
# LOAD CONFIG
# =========================================================

def load_config(config_path):

    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found: {config_path}"
        )

    with open(
        config_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    # -----------------------------------------------------
    # Required Sections
    # -----------------------------------------------------

    data.setdefault("boxes", {})
    data.setdefault("style", {})
    data.setdefault("output", {})

    # -----------------------------------------------------
    # Required Boxes
    # -----------------------------------------------------

    defaults = {

        "question": [70, 150, 460, 180],

        "answer": [120, 350, 360, 100],

        "subject": [70, 35, 240, 40],

        "stage": [390, 35, 90, 40],
    }

    for key, value in defaults.items():
        data["boxes"].setdefault(key, value)

    # -----------------------------------------------------
    # Required Style Sections
    # -----------------------------------------------------

    for section in (

        "question",

        "answer",

        "subject",

        "stage",

    ):

        data["style"].setdefault(section, {})

    # Subject defaults

    subject = data["style"]["subject"]

    subject.setdefault("font_size", 24)
    subject.setdefault("fill", "#FFFFFF")
    subject.setdefault("stroke_fill", "#000000")
    subject.setdefault("stroke_width", 2)
    subject.setdefault("bold", False)
    subject.setdefault("italic", False)

    # Stage defaults

    stage = data["style"]["stage"]

    stage.setdefault("font_size", 24)
    stage.setdefault("fill", "#FFFFFF")
    stage.setdefault("stroke_fill", "#000000")
    stage.setdefault("stroke_width", 2)
    stage.setdefault("bold", False)
    stage.setdefault("italic", False)

    return Config(data)