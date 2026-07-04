import tkinter as tk
from tkinter import ttk, colorchooser
from pathlib import Path


# =========================================================
# FILE SELECTOR WIDGET
# =========================================================
class FileSelector(ttk.Frame):
    """
    Reusable file/folder picker widget.
    """

    def __init__(
        self,
        master,
        label="Select File",
        filetypes=None,
        folder=False,
        command=None,
        width=40,
    ):
        super().__init__(master)

        self.filetypes = filetypes
        self.folder = folder
        self.command = command
        self.path = None

        ttk.Label(self, text=label, width=18).pack(side="left")

        self.label = ttk.Label(self, text="Not selected", width=width)
        self.label.pack(side="left", padx=5)

        ttk.Button(self, text="Browse", command=self.browse).pack(side="right")

    def browse(self):
        if self.folder:
            path = tk.filedialog.askdirectory()
        else:
            path = tk.filedialog.askopenfilename(filetypes=self.filetypes)

        if path:
            self.path = Path(path)
            self.label.config(text=self.path.name)

            if self.command:
                self.command(self.path)


# =========================================================
# COLOR PICKER WIDGET (MODERN SWATCH STYLE)
# =========================================================
class ColorPicker(ttk.Frame):
    """
    Color selector with visual preview.
    """

    def __init__(self, master, label="Color", default="#FFFFFF", callback=None):
        super().__init__(master)

        self.callback = callback
        self.color = default

        ttk.Label(self, text=label, width=18).pack(side="left")

        self.button = tk.Button(
            self,
            bg=self.color,
            width=4,
            command=self.pick_color,
            relief="flat",
        )
        self.button.pack(side="left", padx=5)

    def pick_color(self):
        color = colorchooser.askcolor(initialcolor=self.color)[1]

        if color:
            self.color = color
            self.button.config(bg=color)

            if self.callback:
                self.callback(color)


# =========================================================
# TOGGLE SWITCH (ENHANCED CHECKBOX)
# =========================================================
class ToggleSwitch(ttk.Frame):
    """
    Modern boolean toggle control.
    """

    def __init__(self, master, text="Enable", default=True, callback=None):
        super().__init__(master)

        self.var = tk.BooleanVar(value=default)
        self.callback = callback

        self.check = ttk.Checkbutton(
            self,
            text=text,
            variable=self.var,
            command=self.changed,
        )
        self.check.pack(side="left")

    def changed(self):
        if self.callback:
            self.callback(self.var.get())

    def get(self):
        return self.var.get()


# =========================================================
# NUMBER INPUT (SPINBOX WRAPPER)
# =========================================================
class NumberInput(ttk.Frame):
    """
    Numeric input with label + spinbox.
    """

    def __init__(
        self,
        master,
        label="Value",
        variable=None,
        min_value=0,
        max_value=100,
        step=1,
    ):
        super().__init__(master)

        self.var = variable or tk.IntVar()

        ttk.Label(self, text=label, width=18).pack(side="left")

        self.spin = ttk.Spinbox(
            self,
            from_=min_value,
            to=max_value,
            increment=step,
            textvariable=self.var,
            width=8,
        )
        self.spin.pack(side="left")

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(value)


# =========================================================
# SLIDER INPUT (MODERN RANGE CONTROL)
# =========================================================
class SliderInput(ttk.Frame):
    """
    Horizontal slider with label.
    """

    def __init__(
        self,
        master,
        label="Slider",
        variable=None,
        min_value=0,
        max_value=100,
        callback=None,
    ):
        super().__init__(master)

        self.var = variable or tk.IntVar()
        self.callback = callback

        ttk.Label(self, text=label, width=18).pack(anchor="w")

        self.slider = ttk.Scale(
            self,
            from_=min_value,
            to=max_value,
            variable=self.var,
            command=self.changed,
        )
        self.slider.pack(fill="x")

    def changed(self, _=None):
        if self.callback:
            self.callback(self.var.get())

    def get(self):
        return self.var.get()


# =========================================================
# COLLAPSIBLE SECTION (PRO UI FEATURE)
# =========================================================
class CollapsibleSection(ttk.Frame):
    """
    Expand/collapse container for sidebar groups.
    """

    def __init__(self, master, title="Section"):
        super().__init__(master)

        self.expanded = True

        self.header = ttk.Frame(self)
        self.header.pack(fill="x")

        self.btn = ttk.Button(
            self.header,
            text=f"▼ {title}",
            command=self.toggle,
            width=20,
        )
        self.btn.pack(fill="x")

        self.body = ttk.Frame(self)
        self.body.pack(fill="x", pady=5)

    def toggle(self):
        if self.expanded:
            self.body.forget()
            self.btn.config(text=self.btn.cget("text").replace("▼", "►"))
        else:
            self.body.pack(fill="x", pady=5)
            self.btn.config(text=self.btn.cget("text").replace("►", "▼"))

        self.expanded = not self.expanded


# =========================================================
# INPUT ROW HELPER (CLEAN FORM LAYOUT)
# =========================================================
class InputRow(ttk.Frame):
    """
    Label + widget row helper for clean forms.
    """

    def __init__(self, master, label, widget):
        super().__init__(master)

        ttk.Label(self, text=label, width=18).pack(side="left")
        widget.pack(side="left", fill="x", expand=True)