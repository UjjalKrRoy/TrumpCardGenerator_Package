from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from src.text_engine import draw_text_box


# =========================================================
# FONT RESOLVER
# =========================================================
def resolve_font(font_input):
    """
    Resolves font input into a usable PIL font path or family.

    Supports:
    - Full .ttf path
    - System-installed font name (fallback)
    """

    if not font_input:
        raise ValueError("Font input is required")

    font_path = Path(str(font_input))

    if font_path.exists():
        return str(font_path)

    # fallback: system font name (PIL will try best match)
    return str(font_input)


# =========================================================
# CORE RENDER ENGINE
# =========================================================
def create_card(
    question,
    answer,
    output_file,
    config,
    template_path,
    font_path,
    preview=False,
):
    """
    Renders a flashcard image.

    Parameters
    ----------
    question : str
    answer : str
    output_file : Path | None
    config : Config object
    template_path : image background
    font_path : font family or ttf path
    preview : bool (if True → returns PIL Image only)
    """

    template_path = Path(template_path)

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    # -----------------------------------------------------
    # LOAD TEMPLATE
    # -----------------------------------------------------
    image = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(image)

    # -----------------------------------------------------
    # FONT
    # -----------------------------------------------------
    font_path = resolve_font(font_path)

    # -----------------------------------------------------
    # CONFIG
    # -----------------------------------------------------
    q_style = config.get_style("question")
    a_style = config.get_style("answer")

    q_box = list(config.get_box("question"))
    a_box = list(config.get_box("answer"))

    # Optional offsets (safe handling)
    q_offset = q_style.get("offset_y", 0)
    a_offset = a_style.get("offset_y", 0)

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

    # =====================================================
    # RETURN PREVIEW IMAGE
    # =====================================================
    if preview:
        return image

    # =====================================================
    # EXPORT MODE
    # =====================================================
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