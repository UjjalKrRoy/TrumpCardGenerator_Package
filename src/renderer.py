from pathlib import Path

from PIL import Image, ImageDraw

from src.text_engine import draw_text_box


def create_card(
    question,
    answer,
    output_file,
    config,
    template_path,
    font_path,
):
    """
    Creates a single card image.

    Parameters
    ----------
    question : str
    answer : str
    output_file : str | Path
    config : Config
    template_path : str | Path
    font_path : str | Path
    """

    template_path = Path(template_path)
    font_path = Path(font_path)
    output_file = Path(output_file)

    # ----------------------------
    # Validate files
    # ----------------------------
    if not template_path.exists():
        raise FileNotFoundError(
            f"Template image not found:\n{template_path}"
        )

    if not font_path.exists():
        raise FileNotFoundError(
            f"Font file not found:\n{font_path}"
        )

    # ----------------------------
    # Load template
    # ----------------------------
    image = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(image)

    # ----------------------------
    # Draw Question
    # ----------------------------
    q_style = config.get_style("question")

    draw_text_box(
        draw=draw,
        text=question,
        box=tuple(config.get_box("question")),
        font_path=str(font_path),
        max_font_size=q_style.get("font_max", 32),
        min_font_size=q_style.get("font_min", 18),
        fill=q_style.get("fill", "white"),
        stroke_width=q_style.get("stroke_width", 2),
        stroke_fill=q_style.get("stroke_fill", "black"),
    )

    # ----------------------------
    # Draw Answer
    # ----------------------------
    a_style = config.get_style("answer")

    draw_text_box(
        draw=draw,
        text=answer,
        box=tuple(config.get_box("answer")),
        font_path=str(font_path),
        max_font_size=a_style.get("font_max", 28),
        min_font_size=a_style.get("font_min", 18),
        fill=a_style.get("fill", "white"),
        stroke_width=a_style.get("stroke_width", 2),
        stroke_fill=a_style.get("stroke_fill", "black"),
    )

    # ----------------------------
    # Save Image
    # ----------------------------
    output_file.parent.mkdir(parents=True, exist_ok=True)

    image.save(output_file)

    return output_file