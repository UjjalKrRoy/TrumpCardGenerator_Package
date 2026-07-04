import tkinter as tk
from tkinter import ttk


class StatusBar(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.text = tk.StringVar(value="Ready")

        self.label = ttk.Label(
            self,
            textvariable=self.text,
            anchor="w",
            relief="sunken"
        )

        self.label.pack(fill="x")

    def set(self, message):

        self.text.set(message)