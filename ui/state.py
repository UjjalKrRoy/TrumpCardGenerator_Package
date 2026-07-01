from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Callable


# =========================================================
# RUNTIME APPLICATION STATE
# =========================================================
@dataclass
class AppState:
    """
    Central runtime state container for the entire app.

    This is NOT persistent storage.
    This is NOT rendering config.

    It is ONLY live UI + session state.
    """

    # ---------------- FILES ----------------
    template_path: Optional[Path] = None
    excel_path: Optional[Path] = None
    output_dir: Optional[Path] = None
    font_path: Optional[str] = None

    # ---------------- PREVIEW ----------------
    preview_question: str = "Sample Question"
    preview_answer: str = "Sample Answer"

    # ---------------- UI FLAGS ----------------
    is_generating: bool = False
    auto_preview: bool = True

    # ---------------- OFFSET CONTROL ----------------
    question_offset_y: int = 0
    answer_offset_y: int = 0

    # ---------------- CALLBACK HOOKS ----------------
    """
    These allow GUI to react automatically when state changes.
    Example: update preview when values change.
    """

    on_change: Optional[Callable[[str, any], None]] = None

    # =====================================================
    # INTERNAL STATE UPDATE METHOD
    # =====================================================
    def set(self, key: str, value):
        """
        Generic state setter with optional callback hook.
        """

        if not hasattr(self, key):
            raise AttributeError(f"Invalid state key: {key}")

        setattr(self, key, value)

        if self.on_change:
            self.on_change(key, value)

    # =====================================================
    # SAFE GETTER
    # =====================================================
    def get(self, key: str, default=None):
        return getattr(self, key, default)

    # =====================================================
    # FILE HELPERS
    # =====================================================
    def set_template(self, path: str):
        self.template_path = Path(path)

        if self.on_change:
            self.on_change("template_path", self.template_path)

    def set_excel(self, path: str):
        self.excel_path = Path(path)

        if self.on_change:
            self.on_change("excel_path", self.excel_path)

    def set_output(self, path: str):
        self.output_dir = Path(path)

        if self.on_change:
            self.on_change("output_dir", self.output_dir)

    def set_font(self, font: str):
        self.font_path = font

        if self.on_change:
            self.on_change("font_path", self.font_path)

    # =====================================================
    # PREVIEW STATE HELPERS
    # =====================================================
    def update_preview_text(self, question: str, answer: str):
        self.preview_question = question
        self.preview_answer = answer

        if self.on_change:
            self.on_change("preview", (question, answer))

    # =====================================================
    # GENERATION STATE HELPERS
    # =====================================================
    def start_generation(self):
        self.is_generating = True

        if self.on_change:
            self.on_change("is_generating", True)

    def stop_generation(self):
        self.is_generating = False

        if self.on_change:
            self.on_change("is_generating", False)

    # =====================================================
    # OFFSET HELPERS
    # =====================================================
    def set_offsets(self, q_offset: int, a_offset: int):
        self.question_offset_y = q_offset
        self.answer_offset_y = a_offset

        if self.on_change:
            self.on_change("offsets", (q_offset, a_offset))

    # =====================================================
    # RESET STATE
    # =====================================================
    def reset(self):
        self.template_path = None
        self.excel_path = None
        self.output_dir = None
        self.font_path = None

        self.preview_question = "Sample Question"
        self.preview_answer = "Sample Answer"

        self.is_generating = False
        self.auto_preview = True

        self.question_offset_y = 0
        self.answer_offset_y = 0

        if self.on_change:
            self.on_change("reset", None)