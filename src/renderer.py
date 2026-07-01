from pathlib import Path
from PIL import Image, ImageDraw

from src.text_engine import draw_text_box


# =========================================================
# FONT RESOLVER (Word-style support)
# =========================================================
def resolve_font(font_input):
    """
    Accepts:
    - Windows font family (e.g., 'Arial')
    - Full font path (e.g., C:/Windows/Fonts/arial.ttf)
    """

    if font_input is None:
        raise ValueError("Font input is None")

    path = Path(str(font_input))

    # If direct file path
    if path.exists():
        return str(path)

    # Otherwise assume system font name (fallback handled by PIL)
    return str(font_input)


# =========================================================
# MAIN RENDER FUNCTION
# =========================================================
def create_card(
    question,
    answer,
    output_file,
    config,
    template_path,
    font_path,
    q_offset=0,
    a_offset=0,
    preview=False,
):
    """
    Renders a single card or returns preview image.

    Parameters
    ----------
    question : str
    answer : str
    output_file : Path or None
    config : Config
    template_path : Path
    font_path : str (font family OR file path)
    q_offset : int (vertical shift question box)
    a_offset : int (vertical shift answer box)
    preview : bool
    """

    template_path = Path(template_path)

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    # -----------------------------------------------------
    # Load image template
    # -----------------------------------------------------
    image = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(image)

    # -----------------------------------------------------
    # Resolve font
    # -----------------------------------------------------
    font_path = resolve_font(font_path)

    # -----------------------------------------------------
    # Get config
    # -----------------------------------------------------
    q_style = config.get_style("question")
    a_style = config.get_style("answer")

    q_box = list(config.get_box("question"))
    a_box = list(config.get_box("answer"))

    # -----------------------------------------------------
    # Apply optional offsets (safe, non-destructive)
    # -----------------------------------------------------
    q_box[1] += q_offset
    a_box[1] += a_offset

    # =====================================================
    # DRAW QUESTION
    # =====================================================
    draw_text_box(
        draw=draw,
        text=question,
        box=tuple(q_box),
        font_path=font_path,
        max_font_size=q_style.get("font_max", 32),
        min_font_size=q_style.get("font_min", 18),
        fill=q_style.get("fill", "#FFFFFF"),
        stroke_fill=q_style.get("stroke_fill"),
        stroke_width=q_style.get("stroke_width", 2),
        align="center",
    )

    # =====================================================
    # DRAW ANSWER
    # =====================================================
    draw_text_box(
        draw=draw,
        text=answer,
        box=tuple(a_box),
        font_path=font_path,
        max_font_size=a_style.get("font_max", 28),
        min_font_size=a_style.get("font_min", 20),
        fill=a_style.get("fill", "#FFFFFF"),
        stroke_fill=a_style.get("stroke_fill"),
        stroke_width=a_style.get("stroke_width", 2),
        align="center",
    )

    # -----------------------------------------------------
    # PREVIEW MODE (IMPORTANT FIX)
    # -----------------------------------------------------
    if preview:
        return image

    # -----------------------------------------------------
    # OUTPUT MODE
    # -----------------------------------------------------
    if output_file is None:
        raise ValueError("output_file is required when preview=False")

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    export = config.get_output()

    image_format = export.get("format", "PNG")
    quality = export.get("quality", 100)

    save_kwargs = {"format": image_format}

    if image_format.upper() in ("JPG", "JPEG"):
        image = image.convert("RGB")
        save_kwargs["quality"] = quality

    image.save(output_file, **save_kwargs)

    return output_file