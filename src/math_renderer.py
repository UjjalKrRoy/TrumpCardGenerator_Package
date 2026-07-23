from io import BytesIO

from PIL import Image

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


class MathRenderer:
    """
    Renders LaTeX math expressions into transparent PIL images.
    """

    def __init__(
        self,
        dpi=300,
        fontsize=34
    ):

        self.dpi = dpi
        self.fontsize = fontsize

    def render(
        self,
        latex,
        color="black"
    ):
        """
        Parameters
        ----------
        latex : str
            LaTeX expression WITHOUT the surrounding $ symbols.

        color : str
            Text colour.

        Returns
        -------
        PIL.Image
        """

        # First pass to calculate required image size

        fig = plt.figure(
            figsize=(0.01, 0.01),
            dpi=self.dpi
        )

        fig.patch.set_alpha(0)

        text = fig.text(
            0,
            0,
            f"${latex}$",
            fontsize=self.fontsize,
            color=color
        )

        fig.canvas.draw()

        bbox = text.get_window_extent()

        width = bbox.width / self.dpi
        height = bbox.height / self.dpi

        plt.close(fig)

        # Second pass with correct canvas size

        fig = plt.figure(
            figsize=(width, height),
            dpi=self.dpi
        )

        fig.patch.set_alpha(0)

        plt.axis("off")

        fig.text(
            0,
            0,
            f"${latex}$",
            fontsize=self.fontsize,
            color=color
        )

        buffer = BytesIO()

        plt.savefig(
            buffer,
            format="png",
            transparent=True,
            bbox_inches="tight",
            pad_inches=0
        )

        plt.close(fig)

        buffer.seek(0)

        return Image.open(buffer).convert("RGBA")


renderer = MathRenderer()


def render_formula(
    latex,
    color="black",
    fontsize=34
):
    """
    Simple helper.

    Example
    -------

    img = render_formula(
        r"\\frac{a+b}{2}"
    )
    """

    renderer.fontsize = fontsize

    return renderer.render(
        latex,
        color=color
    )

def normalize_formula(text):
    """
    Convert simple mathematical notation into LaTeX.
    This lets users type formulas naturally.
    """

    if text is None:
        return ""

    text = str(text)

    replacements = {

        "√": r"\sqrt",

        "π": r"\pi",
        "θ": r"\theta",
        "α": r"\alpha",
        "β": r"\beta",
        "γ": r"\gamma",

        "sin": r"\sin",
        "cos": r"\cos",
        "tan": r"\tan",
        "cot": r"\cot",
        "sec": r"\sec",
        "csc": r"\csc",

        "log": r"\log",
        "ln": r"\ln",

        "×": r"\times",
        "÷": r"\div",

        "≤": r"\leq",
        "≥": r"\geq",
        "≠": r"\neq",

        "∞": r"\infty",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text

def is_formula(text):
    """
    Detect whether the supplied string
    should be rendered using LaTeX.
    """

    if text is None:
        return False

    text = str(text).strip()

    if not text:
        return False

    # Existing LaTeX commands
    latex_commands = (

        "\\frac",
        "\\sqrt",
        "\\sin",
        "\\cos",
        "\\tan",
        "\\cot",
        "\\sec",
        "\\csc",

        "\\log",
        "\\ln",

        "\\alpha",
        "\\beta",
        "\\gamma",
        "\\theta",
        "\\pi",
        "\\phi",

        "\\sum",
        "\\prod",
        "\\int",
        "\\lim",

        "\\left",
        "\\right",

        "\\cdot",
        "\\times",
        "\\pm",

        "\\leq",
        "\\geq",
        "\\neq",
        "\\infty"
    )

    if any(cmd in text for cmd in latex_commands):
        return True

    # Detect superscripts/subscripts
    if "^" in text or "_" in text:
        return True

    # Detect fractions written with /
    if "/" in text:
        return True

    # Detect equations
    if "=" in text:
        return True

    # Detect common math operators
    operators = [
        "+",
        "-",
        "×",
        "*",
        "÷",
        "(",
        ")"
    ]

    operator_count = sum(op in text for op in operators)

    # If multiple operators exist,
    # it is very likely a mathematical formula.
    if operator_count >= 2:
        return True

    return False