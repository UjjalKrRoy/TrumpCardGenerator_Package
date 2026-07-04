from tkinter import ttk


class PreviewPanel(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent, padding=10)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=1)

        preview = ttk.LabelFrame(
            self,
            text="Card Preview"
        )

        preview.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.image = ttk.Label(preview)
        self.image.pack(expand=True)

        log_frame = ttk.LabelFrame(
            self,
            text="Generation Log"
        )

        log_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=10
        )

        from tkinter.scrolledtext import ScrolledText

        self.log = ScrolledText(
            log_frame,
            height=6
        )

        self.log.pack(fill="both", expand=True)