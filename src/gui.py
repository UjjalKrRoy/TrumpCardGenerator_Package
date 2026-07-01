from pathlib import Path
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, colorchooser
from PIL import ImageTk
from openpyxl import load_workbook
from copy import deepcopy

from matplotlib import font_manager

from src.config import load_config
from src.renderer import create_card


# =========================================================
# SYSTEM FONTS
# =========================================================
def get_system_fonts():
    fonts = {}
    for f in font_manager.fontManager.ttflist:
        fonts.setdefault(f.name, f.fname)
    return fonts


# =========================================================
# MAIN APP
# =========================================================
class CardGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Generator Pro")
        self.root.geometry("1200x800")

        base_dir = Path(__file__).resolve().parent.parent
        self.config_obj = load_config(base_dir / "config.json")

        # ---------------- FILES ----------------
        self.template_path = None
        self.excel_path = None
        self.output_dir = None

        # ---------------- FONTS ----------------
        self.font_map = get_system_fonts()
        self.font_names = sorted(self.font_map.keys())
        self.font_var = tk.StringVar(value="Arial")

        # ---------------- STATE ----------------
        self.preview_photo = None
        self.base_boxes = deepcopy(self.config_obj.boxes)

        # ---------------- STYLE ----------------
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

        self.q_offset = tk.IntVar(value=0)
        self.a_offset = tk.IntVar(value=0)

        # =====================================================
        # LAYOUT (3 PANELS)
        # =====================================================
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(root, padding=10)
        self.sidebar.grid(row=0, column=0, sticky="nswe")

        self.preview_area = ttk.Frame(root, padding=10)
        self.preview_area.grid(row=0, column=1, sticky="nswe")

        # =====================================================
        # TOP ACTION BAR
        # =====================================================
        top_bar = ttk.Frame(self.sidebar)
        top_bar.pack(fill="x", pady=5)

        ttk.Button(top_bar, text="Generate", command=self.start_generation).pack(side="right")

        # =====================================================
        # SCROLLABLE SIDEBAR
        # =====================================================
        canvas = tk.Canvas(self.sidebar)
        scrollbar = ttk.Scrollbar(self.sidebar, orient="vertical", command=canvas.yview)

        self.scroll_frame = ttk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # =====================================================
        # BUILD UI SECTIONS
        # =====================================================
        self.build_project_section()
        self.build_font_section()
        self.build_style_section()
        self.build_layout_section()
        self.build_color_section()
        self.build_outline_section()
        self.build_actions_section()

        # =====================================================
        # PREVIEW PANEL
        # =====================================================
        self.preview_label = ttk.Label(self.preview_area)
        self.preview_label.pack(expand=True)

        self.log_box = scrolledtext.ScrolledText(self.preview_area, height=10)
        self.log_box.pack(fill="x", pady=10)

    # =====================================================
    # UI SECTIONS
    # =====================================================

    def section(self, title):
        frame = ttk.LabelFrame(self.scroll_frame, text=title, padding=10)
        frame.pack(fill="x", pady=8)
        return frame

    # ---------------- PROJECT ----------------
    def build_project_section(self):
        f = self.section("Project")

        ttk.Button(f, text="Template", command=self.select_template).pack(fill="x")
        ttk.Button(f, text="Excel File", command=self.select_excel).pack(fill="x", pady=2)
        ttk.Button(f, text="Output Folder", command=self.select_output).pack(fill="x")

    # ---------------- FONT ----------------
    def build_font_section(self):
        f = self.section("Typography")

        ttk.Label(f, text="Font").pack(anchor="w")

        self.font_dropdown = ttk.Combobox(
            f,
            textvariable=self.font_var,
            values=self.font_names,
            state="readonly"
        )
        self.font_dropdown.pack(fill="x")

    # ---------------- STYLE ----------------
    def build_style_section(self):
        f = self.section("Font Size")

        ttk.Label(f, text="Question Max").pack(anchor="w")
        ttk.Spinbox(f, from_=8, to=120, textvariable=self.q_max).pack(fill="x")

        ttk.Label(f, text="Question Min").pack(anchor="w")
        ttk.Spinbox(f, from_=8, to=120, textvariable=self.q_min).pack(fill="x")

        ttk.Label(f, text="Answer Max").pack(anchor="w")
        ttk.Spinbox(f, from_=8, to=120, textvariable=self.a_max).pack(fill="x")

        ttk.Label(f, text="Answer Min").pack(anchor="w")
        ttk.Spinbox(f, from_=8, to=120, textvariable=self.a_min).pack(fill="x")

    # ---------------- LAYOUT ----------------
    def build_layout_section(self):
        f = self.section("Layout")

        ttk.Label(f, text="Question Y Offset").pack(anchor="w")
        ttk.Spinbox(f, from_=-200, to=200, textvariable=self.q_offset).pack(fill="x")

        ttk.Label(f, text="Answer Y Offset").pack(anchor="w")
        ttk.Spinbox(f, from_=-200, to=200, textvariable=self.a_offset).pack(fill="x")

    # ---------------- COLORS ----------------
    def build_color_section(self):
        f = self.section("Colors")

        ttk.Button(f, text="Question Color", command=self.pick_q_color).pack(fill="x")
        ttk.Button(f, text="Answer Color", command=self.pick_a_color).pack(fill="x")

    # ---------------- OUTLINE ----------------
    def build_outline_section(self):
        f = self.section("Outline")

        ttk.Button(f, text="Question Outline", command=self.pick_q_outline).pack(fill="x")
        ttk.Button(f, text="Answer Outline", command=self.pick_a_outline).pack(fill="x")

    # ---------------- ACTIONS ----------------
    def build_actions_section(self):
        f = self.section("Actions")

        ttk.Button(f, text="Preview", command=self.update_preview).pack(fill="x")
        ttk.Button(f, text="Generate Cards", command=self.start_generation).pack(fill="x", pady=5)

    # =====================================================
    # FILE PICKERS
    # =====================================================

    def select_template(self):
        f = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if f:
            self.template_path = Path(f)
            self.update_preview()

    def select_excel(self):
        f = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if f:
            self.excel_path = Path(f)

    def select_output(self):
        f = filedialog.askdirectory()
        if f:
            self.output_dir = Path(f)

    # =====================================================
    # COLORS
    # =====================================================

    def pick_q_color(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.q_fill = c
            self.update_preview()

    def pick_a_color(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.a_fill = c
            self.update_preview()

    def pick_q_outline(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.q_outline = c
            self.update_preview()

    def pick_a_outline(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.a_outline = c
            self.update_preview()

    # =====================================================
    # PREVIEW
    # =====================================================

    def update_preview(self):
        if not self.template_path:
            return

        config = deepcopy(self.config_obj)

        q = self.base_boxes["question"]
        a = self.base_boxes["answer"]

        config.boxes["question"] = [q[0], q[1] + self.q_offset.get(), q[2], q[3]]
        config.boxes["answer"] = [a[0], a[1] + self.a_offset.get(), a[2], a[3]]

        config.style["question"]["font_max"] = self.q_max.get()
        config.style["question"]["font_min"] = self.q_min.get()
        config.style["answer"]["font_max"] = self.a_max.get()
        config.style["answer"]["font_min"] = self.a_min.get()

        config.style["question"]["fill"] = self.q_fill
        config.style["answer"]["fill"] = self.a_fill

        image = create_card(
            "Sample Question",
            "Sample Answer",
            None,
            config,
            self.template_path,
            self.font_map.get(self.font_var.get(), "Arial"),
            preview=True,
        )

        image.thumbnail((400, 550))

        self.preview_photo = ImageTk.PhotoImage(image)
        self.preview_label.configure(image=self.preview_photo)

    # =====================================================
    # GENERATION
    # =====================================================

    def start_generation(self):
        threading.Thread(target=self.generate_cards, daemon=True).start()

    def generate_cards(self):
        if not all([self.template_path, self.excel_path, self.output_dir]):
            self.root.after(0, lambda: messagebox.showerror("Error", "Missing inputs"))
            return

        wb = load_workbook(self.excel_path)
        ws = wb.active

        self.output_dir.mkdir(exist_ok=True)

        for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 1):
            if not row or not row[0] or not row[1]:
                continue

            create_card(
                str(row[0]),
                str(row[1]),
                self.output_dir / f"Card_{i:03}.png",
                self.config_obj,
                self.template_path,
                self.font_map.get(self.font_var.get(), "Arial"),
            )

            self.log(f"Generated Card_{i:03}.png")

        self.root.after(0, lambda: messagebox.showinfo("Done", "Generation complete"))

    # =====================================================
    # LOGGING
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
    CardGeneratorGUI(root)
    root.mainloop()