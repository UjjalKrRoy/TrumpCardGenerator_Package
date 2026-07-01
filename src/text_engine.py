from PIL import ImageFont


def wrap_text(draw, text, font, max_width):
    """
    Breaks text into multiple lines so each line fits within max_width.
    """

    words = str(text).split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word

        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def draw_text_box(
    draw,
    text,
    box,
    font_path,
    max_font_size=32,
    min_font_size=16,
    fill="white",
    stroke_fill="black",
    stroke_width=2
):
    """
    Auto-fits text inside a bounding box:
    - reduces font size if needed
    - wraps text
    - centers vertically and horizontally
    """

    x, y, w, h = box

    # -----------------------
    # Find best font size
    # -----------------------
    for size in range(max_font_size, min_font_size - 1, -1):

        font = ImageFont.truetype(font_path, size)

        lines = wrap_text(draw, text, font, w)

        line_height = font.getbbox("Ay")[3] + 6
        total_height = len(lines) * line_height

        # check if fits vertically
        if total_height <= h:
            break

    # -----------------------
    # Fallback safety
    # -----------------------
    if not lines:
        lines = [str(text)]
        font = ImageFont.truetype(font_path, min_font_size)
        line_height = font.getbbox("Ay")[3] + 6
        total_height = line_height

    # -----------------------
    # Center vertically
    # -----------------------
    current_y = y + (h - total_height) // 2

    for line in lines:

        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]

        current_x = x + (w - line_width) // 2

        draw.text(
            (current_x, current_y),
            line,
            font=font,
            fill=fill,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill
        )

        current_y += line_height