import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
from pathlib import Path


class FileSelector(ttk.Frame):
    """
    Reusable file/folder picker.
    """

    def __init__(
        self,
        master,
        text,
        command=None,
        filetypes=None,
        folder=False,
        width=45,
    ):
        super().__init__(master)

        self.command = command
        self.filetypes = filetypes
        self.folder = folder
        self.path = None

        ttk.Label(
            self,
            text=text,
            width=15
        ).pack(side="left")

        self.label = ttk.Label(
            self,
            text="Not Selected",
            width=width
        )

        self.label.pack(
            side="left",
            padx=5
        )

        ttk.Button(
            self,
            text="Browse",
            command=self.browse,
            width=10
        ).pack(side="right")

    def browse(self):

        if self.folder:
            filename = filedialog.askdirectory()

        else:
            filename = filedialog.askopenfilename(
                filetypes=self.filetypes
            )

        if filename:

            self.path = Path(filename)

            self.label.config(
                text=self.path.name
            )

            if self.command:
                self.command(self.path)


class ColorPicker(ttk.Frame):

    def __init__(
        self,
        master,
        text,
        default="#FFFFFF",
        callback=None,
    ):
        super().__init__(master)

        self.callback = callback
        self.color = default

        ttk.Label(
            self,
            text=text,
            width=18,
        ).pack(side="left")

        self.button = tk.Button(
            self,
            width=4,
            bg=self.color,
            command=self.pick,
        )

        self.button.pack(
            side="left",
            padx=5,
        )

    def pick(self):

        color = colorchooser.askcolor(
            color=self.color
        )[1]

        if color:

            self.color = color

            self.button.configure(
                bg=color
            )

            if self.callback:
                self.callback(color)

class OutlinePicker(ttk.Frame):

    def __init__(
        self,
        master,
        text,
        default="#000000",
        callback=None,
    ):
        super().__init__(master)

        self.callback = callback

        self.enabled = tk.BooleanVar(
            value=True
        )

        self.color = default

        ttk.Label(
            self,
            text=text,
            width=18,
        ).pack(side="left")

        self.button = tk.Button(
            self,
            bg=self.color,
            width=4,
            command=self.pick,
        )

        self.button.pack(
            side="left",
            padx=5,
        )

        ttk.Checkbutton(
            self,
            text="Outline",
            variable=self.enabled,
            command=self.changed,
        ).pack(side="left")

    def pick(self):

        color = colorchooser.askcolor(
            color=self.color
        )[1]

        if color:

            self.color = color

            self.button.configure(
                bg=color
            )

            self.changed()

    def changed(self):

        if self.callback:

            if self.enabled.get():

                self.callback(self.color)

            else:

                self.callback(None)

class NumberInput(ttk.Frame):

    def __init__(
        self,
        master,
        text,
        variable,
        minimum=8,
        maximum=100,
    ):
        super().__init__(master)

        ttk.Label(
            self,
            text=text,
            width=18,
        ).pack(side="left")

        ttk.Spinbox(
            self,
            from_=minimum,
            to=maximum,
            textvariable=variable,
            width=6,
        ).pack(side="left")