from pathlib import Path
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, colorchooser
from PIL import ImageTk
from openpyxl import load_workbook

from matplotlib import font_manager

from src.config import load_config
from src.renderer import create_card


# ---------------------------------------------------------
# Font resolver (MS Word style system font access)
# ---------------------------------------------------------
def get_system_fonts():
    fonts = {}
    for f in font_manager.fontManager.ttflist:
        if f.name not in fonts:
            fonts[f.name] = f.fname
    return fonts


class CardGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Generator (Word Style Fonts)")
        self.root.geometry("980x750")

        base_dir = Path(__file__).resolve().parent.parent
        self.config_obj = load_config(base_dir / "config.json")

        # ---------------- Paths ----------------
        self.template_path = None
        self.excel_path = None
        self.output_dir = None

        # ---------------- Fonts (WORD STYLE) ----------------
        self.font_map = get_system_fonts()
        self.font_names = sorted(self.font_map.keys())
        self.font_var = tk.StringVar(value="Arial")  # default

        # ---------------- Config ----------------
        q = self.config_obj.get_style("question")
        a = self.config_obj.get_style("answer")

        self.q_max = tk.IntVar(value=q.get("font_max", 32))
        self.q_min = tk.IntVar(value=q.get("font_min", 18))
        self.a_max = tk.IntVar(value=a.get("font_max", 28))
        self.a_min = tk.IntVar(value=a.get("font_min", 20))

        self.q_fill = q.get("fill", "#FFFFFF")
        self.a_fill = a.get("fill", "#FFFFFF")

        self.q_outline = q.get("stroke_fill", "#000000")
        self.a_outline = a.get("stroke_fill", "#000000")

        self.q_outline_enabled = tk.BooleanVar(value=True)
        self.a_outline_enabled = tk.BooleanVar(value=True)

        self.preview_photo = None

        # ---------------- UI ----------------
        frm = ttk.Frame(root, padding=10)
        frm.pack(fill="both", expand=True)
        self.frm = frm

        # ---------------- File inputs ----------------
        self.lbl_template = self._row(frm, 0, "Template", self.select_template)
        self.lbl_excel = self._row(frm, 1, "Excel", self.select_excel)
        self.lbl_output = self._row(frm, 2, "Output", self.select_output)

        # ---------------- FONT DROPDOWN (MS WORD STYLE) ----------------
        ttk.Label(frm, text="Font").grid(row=3, column=0, sticky="w")

        self.font_dropdown = ttk.Combobox(
            frm,
            textvariable=self.font_var,
            values=self.font_names,
            state="readonly",
            width=35
        )
        self.font_dropdown.grid(row=3, column=1, sticky="w")
        self.font_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_preview())

        # ---------------- Font sizes ----------------
        self._spin(frm, 4, "Question Max", self.q_max)
        self._spin(frm, 5, "Question Min", self.q_min)
        self._spin(frm, 6, "Answer Max", self.a_max)
        self._spin(frm, 7, "Answer Min", self.a_min)

        # ---------------- Colors ----------------
        ttk.Label(frm, text="Question Color").grid(row=8, column=0, sticky="w")
        self.btn_q_color = tk.Button(frm, bg=self.q_fill, width=4, command=self.pick_q_color)
        self.btn_q_color.grid(row=8, column=1, sticky="w")

        ttk.Label(frm, text="Answer Color").grid(row=9, column=0, sticky="w")
        self.btn_a_color = tk.Button(frm, bg=self.a_fill, width=4, command=self.pick_a_color)
        self.btn_a_color.grid(row=9, column=1, sticky="w")

        # ---------------- Outline ----------------
        ttk.Label(frm, text="Question Outline").grid(row=10, column=0, sticky="w")
        self.btn_q_outline = tk.Button(frm, bg=self.q_outline, width=4, command=self.pick_q_outline)
        self.btn_q_outline.grid(row=10, column=1)

        ttk.Checkbutton(frm, text="Enable", variable=self.q_outline_enabled,
                        command=self.update_preview).grid(row=10, column=2)

        ttk.Label(frm, text="Answer Outline").grid(row=11, column=0, sticky="w")
        self.btn_a_outline = tk.Button(frm, bg=self.a_outline, width=4, command=self.pick_a_outline)
        self.btn_a_outline.grid(row=11, column=1)

        ttk.Checkbutton(frm, text="Enable", variable=self.a_outline_enabled,
                        command=self.update_preview).grid(row=11, column=2)

        # ---------------- Buttons ----------------
        ttk.Button(frm, text="Generate", command=self.start_generation)\
            .grid(row=12, column=0, pady=10)

        ttk.Button(frm, text="Preview", command=self.update_preview)\
            .grid(row=12, column=1)

        # ---------------- Preview ----------------
        self.preview_label = ttk.Label(frm)
        self.preview_label.grid(row=13, column=0, columnspan=3, pady=10)

        # ---------------- Log ----------------
        self.log_box = scrolledtext.ScrolledText(frm, height=12)
        self.log_box.grid(row=14, column=0, columnspan=3, sticky="nsew")

    # =====================================================
    # Helpers
    # =====================================================

    def _row(self, parent, r, text, cmd):
        ttk.Label(parent, text=text, width=12).grid(row=r, column=0, sticky="w")
        lbl = ttk.Label(parent, text="Not selected", width=40)
        lbl.grid(row=r, column=1, sticky="w")
        ttk.Button(parent, text="Browse", command=cmd).grid(row=r, column=2)
        return lbl

    def _spin(self, parent, r, text, var):
        ttk.Label(parent, text=text).grid(row=r, column=0, sticky="w")
        ttk.Spinbox(parent, from_=8, to=120, textvariable=var, width=6)\
            .grid(row=r, column=1, sticky="w")

    # =====================================================
    # File selection
    # =====================================================

    def select_template(self):
        f = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if f:
            self.template_path = Path(f)
            self.lbl_template.config(text=self.template_path.name)
            self.update_preview()

    def select_excel(self):
        f = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if f:
            self.excel_path = Path(f)
            self.lbl_excel.config(text=self.excel_path.name)

    def select_output(self):
        f = filedialog.askdirectory()
        if f:
            self.output_dir = Path(f)
            self.lbl_output.config(text=str(self.output_dir))

    # =====================================================
    # Colors
    # =====================================================

    def pick_q_color(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.q_fill = c
            self.btn_q_color.config(bg=c)
            self.update_preview()

    def pick_a_color(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.a_fill = c
            self.btn_a_color.config(bg=c)
            self.update_preview()

    def pick_q_outline(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.q_outline = c
            self.btn_q_outline.config(bg=c)
            self.update_preview()

    def pick_a_outline(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.a_outline = c
            self.btn_a_outline.config(bg=c)
            self.update_preview()

    # =====================================================
    # Preview (IMPORTANT FIX AREA)
    # =====================================================

    def update_preview(self):
        if not self.template_path:
            return

        # PUSH UI STATE → CONFIG
        self.config_obj.style["question"]["font_max"] = self.q_max.get()
        self.config_obj.style["question"]["font_min"] = self.q_min.get()
        self.config_obj.style["answer"]["font_max"] = self.a_max.get()
        self.config_obj.style["answer"]["font_min"] = self.a_min.get()

        self.config_obj.style["question"]["fill"] = self.q_fill
        self.config_obj.style["answer"]["fill"] = self.a_fill

        self.config_obj.style["question"]["stroke_fill"] = (
            self.q_outline if self.q_outline_enabled.get() else None
        )
        self.config_obj.style["answer"]["stroke_fill"] = (
            self.a_outline if self.a_outline_enabled.get() else None
        )

        image = create_card(
            "Sample Question",
            "Sample Answer",
            output_file=None,
            config=self.config_obj,
            template_path=self.template_path,
            font_path=self.font_map.get(self.font_var.get(), None),
            preview=True,
        )

        image.thumbnail((320, 450))

        self.preview_photo = ImageTk.PhotoImage(image)
        self.preview_label.configure(image=self.preview_photo)

    # =====================================================
    # Generation
    # =====================================================

    def start_generation(self):
        threading.Thread(target=self.generate_cards, daemon=True).start()

    def generate_cards(self):
        if not all([self.template_path, self.excel_path, self.output_dir]):
            self.root.after(0, lambda: messagebox.showerror("Error", "Missing inputs"))
            return

        font_path = self.font_map.get(self.font_var.get(), None)

        wb = load_workbook(self.excel_path)
        ws = wb.active
        self.output_dir.mkdir(exist_ok=True)

        count = 0

        for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 1):
            if not row or not row[0] or not row[1]:
                continue

            create_card(
                str(row[0]),
                str(row[1]),
                self.output_dir / f"Card_{i:03}.png",
                self.config_obj,
                self.template_path,
                font_path,
            )

            self.log(f"Generated Card_{i:03}.png")
            count += 1

        self.root.after(0, lambda: messagebox.showinfo("Done", f"{count} cards generated"))

    # =====================================================
    # Logging
    # =====================================================

    def log(self, msg):
        self.root.after(
            0,
            lambda: (
                self.log_box.insert("end", msg + "\n"),
                self.log_box.see("end")
            )
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = CardGeneratorGUI(root)
    root.mainloop()