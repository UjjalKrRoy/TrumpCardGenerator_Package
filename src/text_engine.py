from PIL import ImageFont
from src.font_manager import get_font
from pathlib import Path

# =========================================================
# FONT FACTORY
# =========================================================
def load_font(font_path, size, bold=False, italic=False):

    actual_font = get_font(
        font_path,
        bold=bold,
        italic=italic,
    )

    return ImageFont.truetype(
        actual_font,
        size,
    )
# =========================================================
# TEXT WRAPPING
# =========================================================

def wrap_text(
    draw,
    text,
    font,
    max_width,
):

    if not text:
        return [""]

    words = str(text).split()

    lines = []

    current = ""

    for word in words:

        test = word if current == "" else current + " " + word

        bbox = draw.textbbox(
            (0, 0),
            test,
            font=font,
        )

        width = bbox[2] - bbox[0]

        if width <= max_width:

            current = test

        else:

            if current:

                lines.append(current)

            current = word

    if current:

        lines.append(current)

    return lines if lines else [""]


# =========================================================
# AUTO FIT TEXT BOX
# =========================================================

def draw_text_box(

    draw,

    text,

    box,

    font_path,

    max_font_size=32,

    min_font_size=18,

    fill="#FFFFFF",

    stroke_fill="#000000",

    stroke_width=2,

    align="center",

    line_spacing=6,

    margin_left=0,

    margin_right=0,

    margin_top=0,

    margin_bottom=0,

    bold=False,

    italic=False,
):
    """
    Draws multiline text inside a box.

    Features

    • Auto font scaling
    • Word wrap
    • Margins
    • Bold
    • Italic
    • Stroke
    """

    x, y, w, h = box

    x += margin_left
    y += margin_top

    w -= (margin_left + margin_right)
    h -= (margin_top + margin_bottom)

    if w < 10:
        w = 10

    if h < 10:
        h = 10

    text = "" if text is None else str(text)

    best_font = None
    best_lines = [""]

    # ------------------------------------------
    # Largest font that fits
    # ------------------------------------------

    for size in range(max_font_size, min_font_size - 1, -1):

        font = load_font(
            font_path,
            size,
            bold,
            italic,
        )

        lines = wrap_text(
            draw,
            text,
            font,
            w,
        )

        line_height = font.getbbox("Ay")[3] + line_spacing

        total_height = len(lines) * line_height

        if total_height <= h:

            best_font = font
            best_lines = lines
            break

    if best_font is None:

        best_font = load_font(
            font_path,
            min_font_size,
            bold,
            italic,
        )

        best_lines = wrap_text(
            draw,
            text,
            best_font,
            w,
        )

    font = best_font

    line_height = font.getbbox("Ay")[3] + line_spacing

    total_height = len(best_lines) * line_height

    current_y = y + (h - total_height) // 2

    for line in best_lines:

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=font,
        )

        width = bbox[2] - bbox[0]

        if align == "left":

            current_x = x

        elif align == "right":

            current_x = x + w - width

        else:

            current_x = x + (w - width) // 2

        if stroke_width <= 0 or stroke_fill is None:

            draw.text(
                (current_x, current_y),
                line,
                font=font,
                fill=fill,
            )

        else:

            draw.text(
                (current_x, current_y),
                line,
                font=font,
                fill=fill,
                stroke_width=stroke_width,
                stroke_fill=stroke_fill,
            )

        current_y += line_height

    return font


# =========================================================
# FIXED SIZE TEXT
# =========================================================

def draw_single_text(

    draw,

    text,

    box,

    font_path,

    font_size,

    fill="#FFFFFF",

    stroke_fill="#000000",

    stroke_width=2,

    align="center",

    bold=False,

    italic=False,
):
    """
    Used for Subject and Stage.

    Does NOT auto-scale.

    Always uses the chosen font size.
    """

    x, y, w, h = box

    font = load_font(
        font_path,
        font_size,
        bold,
        italic,
    )

    bbox = draw.textbbox(
        (0, 0),
        str(text),
        font=font,
    )

    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    if align == "left":

        tx = x

    elif align == "right":

        tx = x + w - text_w

    else:

        tx = x + (w - text_w) // 2

    ty = y + (h - text_h) // 2

    draw.text(

        (tx, ty),

        str(text),

        font=font,

        fill=fill,

        stroke_width=stroke_width,

        stroke_fill=stroke_fill,

    )

    return font