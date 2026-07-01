import json
from pathlib import Path


class Config:
    """
    Structured configuration wrapper.
    Contains only rendering/layout settings.
    """

    def __init__(self, data: dict):
        self._data = data

        self.boxes = data["boxes"]
        self.style = data.get("style", {})
        self.export = data.get("export", {})

    def get_box(self, name: str):
        """
        Returns a box definition.
        Example:
        question -> [70,150,460,180]
        """
        if name not in self.boxes:
            raise KeyError(f"Box '{name}' not found in config.")

        return self.boxes[name]

    def get_style(self, name: str):
        """
        Returns style dictionary.
        """
        return self.style.get(name, {})


def load_config(config_path: Path) -> Config:
    """
    Loads config.json and performs basic validation.
    """

    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found:\n{config_path}"
        )

    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ---------------- Validation ----------------

    if "boxes" not in data:
        raise KeyError("Missing 'boxes' section in config.json")

    required_boxes = ["question", "answer"]

    for box in required_boxes:
        if box not in data["boxes"]:
            raise KeyError(
                f"Missing '{box}' box in config.json"
            )

    return Config(data)