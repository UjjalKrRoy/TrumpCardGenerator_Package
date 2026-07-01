from pathlib import Path
from PIL import Image, ImageDraw
from matplotlib import font_manager

from src.text_engine import draw_text_box


# ---------------------------------------------------------
# MS Word-style font resolver
# ---------------------------------------------------------
def resolve_font(font_path_or_family):
    """
    Accepts either:
    - system font family name (e.g., Arial)
    - or direct .ttf path
    """

    if font_path_or_family is None:
        raise ValueError("Font is None")

    path = Path(str(font_path_or_family))

    # If already a file path
    if path.exists():
        return str(path)

    # Otherwise treat as font family name
    for f in font_manager.fontManager.ttflist:
        if f.name == font_path_or_family:
            return f.fname

    raise ValueError(f"Font not found: {font_path_or_family}")


# ---------------------------------------------------------
# MAIN RENDER FUNCTION
# ---------------------------------------------------------
def create_card(
    question,
    answer,
    output_file,
    config,
    template_path,
    font_path,
    preview=False
):
    """
    Create a card image or return preview PIL image.
    """

    template_path = Path(template_path)

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    # -----------------------------------------------------
    # Resolve font (MS Word style system font support)
    # -----------------------------------------------------
    font_path = resolve_font(font_path)

    # -----------------------------------------------------
    # Load base image
    # -----------------------------------------------------
    image = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(image)

    # -----------------------------------------------------
    # Get config safely
    # -----------------------------------------------------
    q_style = config.get_style("question")
    a_style = config.get_style("answer")

    q_box = tuple(config.get_box("question"))
    a_box = tuple(config.get_box("answer"))

    # =====================================================
    # QUESTION BOX
    # =====================================================
    draw_text_box(
        draw=draw,
        text=question,
        box=q_box,
        font_path=font_path,
        max_font_size=q_style.get("font_max", 32),
        min_font_size=q_style.get("font_min", 18),
        fill=q_style.get("fill", "#FFFFFF"),
        stroke_fill=q_style.get("stroke_fill"),
        stroke_width=q_style.get("stroke_width", 2),
        align="center",
    )

    # =====================================================
    # ANSWER BOX
    # =====================================================
    draw_text_box(
        draw=draw,
        text=answer,
        box=a_box,
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
        raise ValueError("output_file cannot be None when preview=False")

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