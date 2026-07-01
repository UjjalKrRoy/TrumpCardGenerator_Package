from PIL import ImageFont


def wrap_text(draw, text, font, max_width):
    """
    Wrap text into multiple lines that fit within max_width.
    """

    if not text:
        return [""]

    words = str(text).split()
    lines = []
    current_line = ""

    for word in words:
        test_line = word if not current_line else current_line + " " + word

        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines if lines else [""]


def draw_text_box(
    draw,
    text,
    box,
    font_path,
    max_font_size=32,
    min_font_size=16,
    fill="#FFFFFF",
    stroke_fill="#000000",
    stroke_width=2,
    align="center",
):
    """
    Draw text inside a bounding box with auto font fitting.
    """

    x, y, w, h = box

    text = "" if text is None else str(text)

    best_font = None
    best_lines = [""]

    # ------------------------------------------------
    # Find largest font that fits in box
    # ------------------------------------------------

    for size in range(max_font_size, min_font_size - 1, -1):

        font = ImageFont.truetype(font_path, size)

        lines = wrap_text(draw, text, font, w)

        line_height = font.getbbox("Ay")[3] + 6
        total_height = len(lines) * line_height

        if total_height <= h:
            best_font = font
            best_lines = lines
            break

    # fallback if nothing fits
    if best_font is None:
        best_font = ImageFont.truetype(font_path, min_font_size)
        best_lines = wrap_text(draw, text, best_font, w)

    font = best_font
    lines = best_lines

    line_height = font.getbbox("Ay")[3] + 6
    total_height = len(lines) * line_height

    current_y = y + (h - total_height) // 2

    # ------------------------------------------------
    # Draw lines
    # ------------------------------------------------

    for line in lines:

        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]

        if align == "left":
            current_x = x
        elif align == "right":
            current_x = x + w - line_width
        else:
            current_x = x + (w - line_width) // 2

        # ------------------------------------------------
        # Draw with or without stroke
        # ------------------------------------------------

        if stroke_fill is None or stroke_width <= 0:
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