from matplotlib.font_manager import FontProperties, findfont


def get_font(font_path, bold=False, italic=False):
    family = FontProperties(fname=font_path).get_name()

    prop = FontProperties(
        family=family,
        weight="bold" if bold else "normal",
        style="italic" if italic else "normal",
    )

    return findfont(prop)