from tkinter import ttk


class Toolbar(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=5)

        self.app = app

        ttk.Button(
            self,
            text="Preview",
            command=app.update_preview
        ).pack(side="left", padx=5)

        ttk.Button(
            self,
            text="Generate",
            command=app.start_generation
        ).pack(side="left", padx=5)