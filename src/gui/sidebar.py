from tkinter import ttk


class Sidebar(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent, width=330, padding=10)

        self.grid_propagate(False)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.project_tab = ttk.Frame(self.notebook, padding=10)
        self.style_tab = ttk.Frame(self.notebook, padding=10)
        self.layout_tab = ttk.Frame(self.notebook, padding=10)
        self.color_tab = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.project_tab, text="Project")
        self.notebook.add(self.style_tab, text="Typography")
        self.notebook.add(self.layout_tab, text="Layout")
        self.notebook.add(self.color_tab, text="Colors")

    def section(self, parent, title):

        frame = ttk.LabelFrame(
            parent,
            text=title,
            padding=10
        )

        frame.pack(fill="x", pady=10)

        return frame