import tkinter as tk
from tkinter import ttk


# =========================================================
# BASIC SECTION FACTORY
# =========================================================
def create_section(parent, title):
    """
    Creates a consistent styled section container.
    Used for sidebar grouping.
    """
    frame = ttk.LabelFrame(parent, text=title, padding=10)
    frame.pack(fill="x", pady=8)
    return frame


# =========================================================
# SCROLLABLE SIDEBAR CONTAINER
# =========================================================
def create_scrollable_sidebar(parent):
    """
    Returns a scrollable frame for long control panels.

    Structure:
    Canvas -> Scrollbar -> Inner Frame
    """

    canvas = tk.Canvas(parent, highlightthickness=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)

    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Layout
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scroll_frame


# =========================================================
# MAIN APPLICATION LAYOUT
# =========================================================
def create_main_layout(root):
    """
    Creates the main 2-panel application layout:

    LEFT  -> Controls (Sidebar)
    RIGHT -> Preview + Logs
    """

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)
    root.rowconfigure(0, weight=1)

    # ---------------- LEFT PANEL (SIDEBAR) ----------------
    sidebar = ttk.Frame(root, padding=10)
    sidebar.grid(row=0, column=0, sticky="nswe")

    scrollable = create_scrollable_sidebar(sidebar)

    # ---------------- RIGHT PANEL (PREVIEW) ----------------
    preview_area = ttk.Frame(root, padding=10)
    preview_area.grid(row=0, column=1, sticky="nswe")

    return scrollable, preview_area


# =========================================================
# TOP ACTION BAR
# =========================================================
def create_top_bar(parent):
    """
    Creates a simple action bar with primary controls.
    """

    bar = ttk.Frame(parent)
    bar.pack(fill="x", pady=5)

    return bar


# =========================================================
# BUTTON FACTORY (CONSISTENT UI STYLE)
# =========================================================
def create_button(parent, text, command=None, primary=False):
    """
    Standard button creator.

    primary=True → used for Generate button
    """

    style = {}

    if primary:
        style["padding"] = 6

    btn = ttk.Button(parent, text=text, command=command)

    btn.pack(fill="x", pady=3)

    return btn


# =========================================================
# LABEL + INPUT ROW HELPER
# =========================================================
def create_input_row(parent, label_text, widget):
    """
    Creates aligned label + input row.
    Used for cleaner forms.
    """

    frame = ttk.Frame(parent)
    frame.pack(fill="x", pady=3)

    ttk.Label(frame, text=label_text, width=18).pack(side="left")
    widget.pack(side="left", fill="x", expand=True)

    return frame


# =========================================================
# SIMPLE TITLE HEADER
# =========================================================
def create_header(parent, title):
    """
    Section header (optional for branding / project name).
    """

    label = ttk.Label(
        parent,
        text=title,
        font=("Arial", 14, "bold")
    )
    label.pack(anchor="w", pady=(0, 10))

    return label