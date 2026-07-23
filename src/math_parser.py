import re


def convert_to_latex(expr: str):

    expr = expr.strip()

    # ------------------------
    # Greek letters
    # ------------------------

    greek = {
        "theta": r"\theta",
        "alpha": r"\alpha",
        "beta": r"\beta",
        "gamma": r"\gamma",
        "lambda": r"\lambda",
        "pi": r"\pi",
        "Delta": r"\Delta",
    }

    for key, value in greek.items():
        expr = re.sub(rf"\b{key}\b", value, expr)

    # ------------------------
    # Trigonometry
    # ------------------------

    expr = re.sub(r"\bsin\b", r"\\sin", expr)
    expr = re.sub(r"\bcos\b", r"\\cos", expr)
    expr = re.sub(r"\btan\b", r"\\tan", expr)
    expr = re.sub(r"\bcot\b", r"\\cot", expr)
    expr = re.sub(r"\bsec\b", r"\\sec", expr)
    expr = re.sub(r"\bcosec\b", r"\\csc", expr)

    # ------------------------
    # Square Root
    # ------------------------

    expr = re.sub(
        r"sqrt\((.*?)\)",
        r"\\sqrt{\1}",
        expr
    )

    # ------------------------
    # Powers
    # ------------------------

    expr = re.sub(
        r'([A-Za-z0-9\)\]])\^([A-Za-z0-9]+)',
        r'\1^{\2}',
        expr
    )

    # ------------------------
    # Subscripts
    # ------------------------

    expr = re.sub(
        r'([A-Za-z])_([A-Za-z0-9]+)',
        r'\1_{\2}',
        expr
    )

    return expr