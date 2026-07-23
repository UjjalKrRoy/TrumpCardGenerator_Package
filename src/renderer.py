from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from src.math_renderer import (
    render_formula,
    is_formula,
)

from src.text_engine import (
    draw_text_box,
    draw_single_text,
)


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
# MATH FORMULA RESOLVER
# =========================================================

def draw_formula_box(
    image,
    latex,
    box,
    fill="#000000",
    font_size=32,
):
    """
    Draw a LaTeX formula centered inside the given box.
    """

    formula = render_formula(
        latex=latex,
        color=fill,
        fontsize=font_size,
    )

    box_x, box_y, box_w, box_h = box

    fw, fh = formula.size

    scale = min(
        box_w / fw,
        box_h / fh,
        1.0,
    )

    if scale < 1:

        formula = formula.resize(
            (
                int(fw * scale),
                int(fh * scale),
            ),
            Image.LANCZOS,
        )

        fw, fh = formula.size

    x = box_x + (box_w - fw) // 2
    y = box_y + (box_h - fh) // 2

    image.alpha_composite(
        formula,
        (x, y),
    )

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
    subject="",
    stage="",
    subject_font_path=None,
    stage_font_path=None,
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

    qa_font = font_path

    subject_font = resolve_font(subject_font_path) if subject_font_path else qa_font
    stage_font = resolve_font(stage_font_path) if stage_font_path else subject_font

    # -----------------------------------------------------
    # CONFIG
    # -----------------------------------------------------
    q_style = config.get_style("question")
    a_style = config.get_style("answer")

    s_style = config.get_style("subject")
    st_style = config.get_style("stage")

    q_box = list(config.get_box("question"))
    a_box = list(config.get_box("answer"))

    subject_box = list(config.get_box("subject"))
    stage_box = list(config.get_box("stage"))

    # Apply Question Margins
    q_box[0] += q_style.get("margin_left", 0)
    q_box[1] += q_style.get("margin_top", 0)
    q_box[2] -= (
        q_style.get("margin_left", 0)
        + q_style.get("margin_right", 0)
    )
    q_box[3] -= (
        q_style.get("margin_top", 0)
        + q_style.get("margin_bottom", 0)
    )

    # Apply Answer Margins
    a_box[0] += a_style.get("margin_left", 0)
    a_box[1] += a_style.get("margin_top", 0)
    a_box[2] -= (
        a_style.get("margin_left", 0)
        + a_style.get("margin_right", 0)
    )
    a_box[3] -= (
        a_style.get("margin_top", 0)
        + a_style.get("margin_bottom", 0)
    )

    # Optional offsets (safe handling)
    q_offset = q_style.get("offset_y", 0)
    a_offset = a_style.get("offset_y", 0)

    q_box[1] += q_offset
    a_box[1] += a_offset

    # =====================================================
    # DRAW QUESTION
    # =====================================================
    if is_formula(question):

        draw_formula_box(
            image=image,
            latex=question,
            box=tuple(q_box),
            fill=q_style.get("fill", "#FFFFFF"),
            font_size=q_style.get("font_max", 32),
        )

    else:

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
            bold=q_style.get("bold", False),
            italic=q_style.get("italic", False),
        )

    # =====================================================
    # DRAW ANSWER
    # =====================================================
    if is_formula(answer):

        draw_formula_box(
            image=image,
            latex=answer,
            box=tuple(a_box),
            fill=a_style.get("fill", "#FFFFFF"),
            font_size=a_style.get("font_max", 28),
        )

    else:

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
            bold=a_style.get("bold", False),
            italic=a_style.get("italic", False),
        )

    # =====================================================
    # SUBJECT
    # =====================================================

    draw_single_text(
        draw=draw,
        text=subject,
        box=subject_box,
        font_path=subject_font,
        font_size=s_style.get("font_size",24),
        fill=s_style.get("fill","#FFFFFF"),
        stroke_fill=s_style.get("stroke_fill","#000000"),
        stroke_width=s_style.get("stroke_width",2),
        align=s_style.get("align", "center"),
        bold=s_style.get("bold",False),
        italic=s_style.get("italic",False),
    )

    # =====================================================
    # STAGE
    # =====================================================

    draw_single_text(
        draw=draw,
        text=stage,
        box=stage_box,
        font_path=stage_font,
        font_size=st_style.get("font_size",24),
        fill=st_style.get("fill","#FFFFFF"),
        stroke_fill=st_style.get("stroke_fill","#000000"),
        stroke_width=st_style.get("stroke_width",2),
        align="center",
        bold=st_style.get("bold",False),
        italic=st_style.get("italic",False),
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