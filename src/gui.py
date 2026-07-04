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
    def create_scrollable_tab(self):
        container = ttk.Frame(self.notebook)

        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )

        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        window = canvas.create_window(
            (0, 0),
            window=scroll_frame,
            anchor="nw"
        )

        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfigure(
                window,
                width=e.width
            )
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _wheel(event):
            canvas.yview_scroll(int(-event.delta / 120), "units")

        scroll_frame.bind(
            "<Enter>",
            lambda e: canvas.bind_all("<MouseWheel>", _wheel)
        )

        scroll_frame.bind(
            "<Leave>",
            lambda e: canvas.unbind_all("<MouseWheel>")
        )

        return container, scroll_frame
    def __init__(self, root):
        self.root = root
        self.root.title("Card Generator Pro")
        
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        width = int(screen_w * 0.9)
        height = int(screen_h * 0.9)

        x = (screen_w - width) // 2
        y = (screen_h - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(1100, 700)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

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

        # Question box resize
        self.q_left = tk.IntVar(value=0)
        self.q_right = tk.IntVar(value=0)
        self.q_top = tk.IntVar(value=0)
        self.q_bottom = tk.IntVar(value=0)

        # Answer box resize
        self.a_left = tk.IntVar(value=0)
        self.a_right = tk.IntVar(value=0)
        self.a_top = tk.IntVar(value=0)
        self.a_bottom = tk.IntVar(value=0)

        self.q_margin_left = tk.IntVar(value=20)
        self.q_margin_right = tk.IntVar(value=20)
        self.q_margin_top = tk.IntVar(value=10)
        self.q_margin_bottom = tk.IntVar(value=10)

        self.a_margin_left = tk.IntVar(value=20)
        self.a_margin_right = tk.IntVar(value=20)
        self.a_margin_top = tk.IntVar(value=10)
        self.a_margin_bottom = tk.IntVar(value=10)

        # Excel row range
        self.start_row = tk.IntVar(value=2)
        self.end_row = tk.IntVar(value=0)   # 0 = last row

        # ==========================
        # Main Frame
        # ==========================

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0,column=0,sticky="nsew")

        self.main_frame.columnconfigure(0, weight=1, minsize=340)
        self.main_frame.columnconfigure(1, weight=3)
        self.main_frame.rowconfigure(0,weight=1)

        self.left_panel = ttk.Frame(
            self.main_frame,
            padding=10,
            width=360
        )

        self.left_panel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.notebook = ttk.Notebook(
            self.left_panel
        )

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=2,
            pady=2
        )

        self.left_panel.pack_propagate(False)
    

       
        self.project_tab = ttk.Frame(self.notebook,padding=10)
        self.style_tab = ttk.Frame(self.notebook,padding=10)
        layout_container, self.layout_tab = self.create_scrollable_tab()
        self.color_tab = ttk.Frame(self.notebook,padding=10)

        self.notebook.add(
            self.project_tab,
            text="Project"
        )

        self.notebook.add(
            self.style_tab,
            text="Typography"
        )

        self.notebook.add(
            layout_container,
            text="Layout"
        )

        self.notebook.add(
            self.color_tab,
            text="Colors"
        )

        self.right_panel = ttk.Frame(
            self.main_frame,
            padding=15
        )

        self.right_panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.right_panel.rowconfigure(0,weight=1)
        self.right_panel.rowconfigure(1,weight=0)
        self.right_panel.columnconfigure(0, weight=1)

       
        # Auto-update preview when values change
        for var in (
            self.q_max,
            self.q_min,
            self.a_max,
            self.a_min,

            self.q_offset,
            self.a_offset,

            self.q_margin_left,
            self.q_margin_right,
            self.q_margin_top,
            self.q_margin_bottom,

            self.a_margin_left,
            self.a_margin_right,
            self.a_margin_top,
            self.a_margin_bottom,

            self.q_left,
            self.q_right,
            self.q_top,
            self.q_bottom,

            self.a_left,
            self.a_right,
            self.a_top,
            self.a_bottom,
        ):
            var.trace_add("write", lambda *args: self.update_preview())
    
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

        preview_frame = ttk.LabelFrame(
            self.right_panel,
            text="Card Preview"
        )

        preview_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        preview_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)

        self.preview_label = ttk.Label(preview_frame)
                
        self.preview_label.pack(fill="both", expand=True, padx=10, pady=10)

        log_frame = ttk.LabelFrame(
            self.right_panel,
            text="Generation Log"
        )

        log_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(10,0)
        )

        self.log_box = scrolledtext.ScrolledText(
            log_frame,
            height=6
        )

        self.log_box.pack(
            fill="both",
            expand=True
        )
        self.status = tk.StringVar(value="Ready")

        ttk.Label(
            self.root,
            textvariable=self.status,
            relief="sunken",
            anchor="w"
        ).grid(
            row=1,
            column=0,
            sticky="ew"
        )
    # =====================================================
    # UI SECTIONS
    # =====================================================

    def section(self,parent,title):

        frame=ttk.LabelFrame(
            parent,
            text=title,
            padding=10
        )

        frame.pack(fill="x", pady=10)

        return frame

    # ---------------- PROJECT ----------------
    def build_project_section(self):
        f = self.section(
            self.project_tab,
            "Project"
        )

        ttk.Button(f, text="Select Template", command=self.select_template).pack(fill="x")
        ttk.Button(f, text="Select Excel File", command=self.select_excel).pack(fill="x", pady=2)
        ttk.Button(f, text="Select Output Folder", command=self.select_output).pack(fill="x")

        ttk.Separator(f, orient="horizontal").pack(fill="x", pady=8)

        ttk.Label(f, text="Start Row").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=2,
            to=100000,
            textvariable=self.start_row
        ).pack(fill="x")

        ttk.Label(f, text="End Row (0 = Last Row)").pack(anchor="w")
        ttk.Label(
            f,
            text="0 = Generate till last row",
            foreground="gray"
        ).pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=0,
            to=100000,
            textvariable=self.end_row
        ).pack(fill="x")

    # ---------------- FONT ----------------
    def build_font_section(self):
        f = self.section(
            self.style_tab,
            "Typography"
        )

        ttk.Label(f, text="Font").pack(anchor="w")

        self.font_dropdown = ttk.Combobox(
            f,
            textvariable=self.font_var,
            values=self.font_names,
            state="readonly"
        )
        self.font_dropdown.pack(fill="x")

        self.font_var.trace_add(
            "write",
            lambda *args: self.update_preview()
        )

    # ---------------- STYLE ----------------
    def build_style_section(self):
        f = self.section(
            self.style_tab,
            "Font Size"
        )

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
        f = self.section(
            self.layout_tab,
            "Layout"
        )

        # ===========================
        # Question
        # ===========================
        ttk.Label(f, text="Question Y Offset").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=-200,
            to=200,
            textvariable=self.q_offset
        ).pack(fill="x")

        ttk.Label(f, text="Question Left Margin").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=0,
            to=100,
            textvariable=self.q_margin_left
        ).pack(fill="x")

        ttk.Label(f, text="Question Right Margin").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=0,
            to=100,
            textvariable=self.q_margin_right
        ).pack(fill="x")

        ttk.Label(f, text="Question Top Margin").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=0,
            to=100,
            textvariable=self.q_margin_top
        ).pack(fill="x")

        ttk.Label(f, text="Question Bottom Margin").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=0,
            to=100,
            textvariable=self.q_margin_bottom
        ).pack(fill="x")

        ttk.Separator(f, orient="horizontal").pack(fill="x", pady=8)

        ttk.Label(f, text="Question Box Left").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=-300,
            to=300,
            textvariable=self.q_left
        ).pack(fill="x")

        ttk.Label(f, text="Question Box Right").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=-300,
            to=300,
            textvariable=self.q_right
        ).pack(fill="x")

        ttk.Label(f, text="Question Box Top").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=-300,
            to=300,
            textvariable=self.q_top
        ).pack(fill="x")

        ttk.Label(f, text="Question Box Bottom").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=-300,
            to=300,
            textvariable=self.q_bottom
        ).pack(fill="x")
        
        ttk.Separator(f, orient="horizontal").pack(fill="x", pady=8)

        # ===========================
        # Answer
        # ===========================
        ttk.Label(f, text="Answer Y Offset").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=-200,
            to=200,
            textvariable=self.a_offset
        ).pack(fill="x")

        ttk.Label(f, text="Answer Left Margin").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=0,
            to=100,
            textvariable=self.a_margin_left
        ).pack(fill="x")

        ttk.Label(f, text="Answer Right Margin").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=0,
            to=100,
            textvariable=self.a_margin_right
        ).pack(fill="x")

        ttk.Label(f, text="Answer Top Margin").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=0,
            to=100,
            textvariable=self.a_margin_top
        ).pack(fill="x")

        ttk.Label(f, text="Answer Bottom Margin").pack(anchor="w")
        
        ttk.Spinbox(
            f,
            from_=0,
            to=100,
            textvariable=self.a_margin_bottom
        ).pack(fill="x")

        ttk.Separator(f, orient="horizontal").pack(fill="x", pady=8)

        ttk.Label(f, text="Answer Box Left").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=-300,
            to=300,
            textvariable=self.a_left
        ).pack(fill="x")

        ttk.Label(f, text="Answer Box Right").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=-300,
            to=300,
            textvariable=self.a_right
        ).pack(fill="x")

        ttk.Label(f, text="Answer Box Top").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=-300,
            to=300,
            textvariable=self.a_top
        ).pack(fill="x")

        ttk.Label(f, text="Answer Box Bottom").pack(anchor="w")
        ttk.Spinbox(
            f,
            from_=-300,
            to=300,
            textvariable=self.a_bottom
        ).pack(fill="x")
        

    # ---------------- COLORS ----------------
    def build_color_section(self):
        f = self.section(
            self.color_tab,
            "Colors"
        )

        ttk.Button(f, text="Question Color", command=self.pick_q_color).pack(fill="x")
        ttk.Button(f, text="Answer Color", command=self.pick_a_color).pack(fill="x")

    # ---------------- OUTLINE ----------------
    def build_outline_section(self):
        f = self.section(
            self.color_tab,
            "Outline"
        )

        ttk.Button(f, text="Question Outline", command=self.pick_q_outline).pack(fill="x")
        ttk.Button(f, text="Answer Outline", command=self.pick_a_outline).pack(fill="x")

    # ---------------- ACTIONS ----------------
    def build_actions_section(self):
        f = self.section(
            self.project_tab,
            "Actions"
        )

        ttk.Button(f, text="Preview", command=self.update_preview).pack(fill="x")
        ttk.Button(f, text="Generate Cards", command=self.start_generation).pack(fill="x", pady=5)

    # =====================================================
    # FILE PICKERS
    # =====================================================

    def select_template(self):
        f = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if f:
            self.template_path = Path(f)
            self.status.set(f"Template: {self.template_path.name}")
            self.update_preview()

    def select_excel(self):
        f = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if f:
            self.excel_path = Path(f)
            self.status.set(f"Excel: {self.excel_path.name}")
            self.update_preview()

    def select_output(self):
        f = filedialog.askdirectory()
        if f:
            self.output_dir = Path(f)
            self.status.set(f"Output: {self.output_dir}")
            self.update_preview()

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

        config.boxes["question"] = [
            q[0] + self.q_left.get(),
            q[1] + self.q_top.get() + self.q_offset.get(),
            q[2] + self.q_right.get(),
            q[3] + self.q_bottom.get(),
        ]
        config.boxes["answer"] = [
            a[0] + self.a_left.get(),
            a[1] + self.a_offset.get() + self.a_top.get(),
            a[2] + self.a_right.get(),
            a[3] + self.a_bottom.get(),
        ]

        config.style["question"]["font_max"] = self.q_max.get()
        config.style["question"]["font_min"] = self.q_min.get()
        config.style["answer"]["font_max"] = self.a_max.get()
        config.style["answer"]["font_min"] = self.a_min.get()

        config.style["question"]["fill"] = self.q_fill
        config.style["answer"]["fill"] = self.a_fill

        config.style["question"]["stroke_fill"] = self.q_outline
        config.style["answer"]["stroke_fill"] = self.a_outline

        # Question margins
        config.style["question"]["margin_left"] = self.q_margin_left.get()
        config.style["question"]["margin_right"] = self.q_margin_right.get()
        config.style["question"]["margin_top"] = self.q_margin_top.get()
        config.style["question"]["margin_bottom"] = self.q_margin_bottom.get()

        # Answer margins
        config.style["answer"]["margin_left"] = self.a_margin_left.get()
        config.style["answer"]["margin_right"] = self.a_margin_right.get()
        config.style["answer"]["margin_top"] = self.a_margin_top.get()
        config.style["answer"]["margin_bottom"] = self.a_margin_bottom.get()

        image = create_card(
            "Sample Question",
            "Sample Answer",
            None,
            config,
            self.template_path,
            self.font_map.get(self.font_var.get(), "Arial"),
            preview=True,
        )

        
        self.preview_label.update_idletasks()

        w = max(self.preview_label.winfo_width() - 20, 300)
        h = max(self.preview_label.winfo_height() - 20, 400)

        image.thumbnail((w, h))

        self.preview_photo = ImageTk.PhotoImage(image)
        self.preview_label.configure(image=self.preview_photo)

    # =====================================================
    # GENERATION
    # =====================================================

    def start_generation(self):
        self.status.set("Generating cards...")
        threading.Thread(target=self.generate_cards, daemon=True).start()

    def generate_cards(self):
        if not all([self.template_path, self.excel_path, self.output_dir]):
            self.root.after(0, lambda: messagebox.showerror("Error", "Missing inputs"))
            return

        wb = load_workbook(self.excel_path)
        ws = wb.active

        config = deepcopy(self.config_obj)

        q = self.base_boxes["question"]
        a = self.base_boxes["answer"]

        config.boxes["question"] = [
            q[0] + self.q_left.get(),
            q[1] + self.q_top.get() + self.q_offset.get(),
            q[2] + self.q_right.get(),
            q[3] + self.q_bottom.get(),
        ]

        config.boxes["answer"] = [
            a[0] + self.a_left.get(),
            a[1] + self.a_offset.get() + self.a_top.get(),
            a[2] + self.a_right.get(),
            a[3] + self.a_bottom.get(),
        ]

        # Fonts
        config.style["question"]["font_max"] = self.q_max.get()
        config.style["question"]["font_min"] = self.q_min.get()

        config.style["answer"]["font_max"] = self.a_max.get()
        config.style["answer"]["font_min"] = self.a_min.get()

        # Colors
        config.style["question"]["fill"] = self.q_fill
        config.style["answer"]["fill"] = self.a_fill

        config.style["question"]["stroke_fill"] = self.q_outline
        config.style["answer"]["stroke_fill"] = self.a_outline

        # Margins
        config.style["question"]["margin_left"] = self.q_margin_left.get()
        config.style["question"]["margin_right"] = self.q_margin_right.get()
        config.style["question"]["margin_top"] = self.q_margin_top.get()
        config.style["question"]["margin_bottom"] = self.q_margin_bottom.get()

        config.style["answer"]["margin_left"] = self.a_margin_left.get()
        config.style["answer"]["margin_right"] = self.a_margin_right.get()
        config.style["answer"]["margin_top"] = self.a_margin_top.get()
        config.style["answer"]["margin_bottom"] = self.a_margin_bottom.get()

        self.output_dir.mkdir(exist_ok=True)

        start = self.start_row.get()
        end = self.end_row.get()

        if end <= 0:
            end = ws.max_row
        
        if start < 2:
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Error",
                    "Start Row must be 2 or greater."
                )
            )
            return

        if start > end:
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Error",
                    "Start Row cannot be greater than End Row."
                )
            )
            return

        if end > ws.max_row:
            end = ws.max_row

        for i, row in enumerate(
            ws.iter_rows(
                min_row=start,
                max_row=end,
                values_only=True
            ),
            start
        ):

            if not row or not row[0] or not row[1]:
                continue

            create_card(
                str(row[0]),
                str(row[1]),
                self.output_dir / f"Card_{i:03}.png",
                config,
                self.template_path,
                self.font_map.get(self.font_var.get(), "Arial"),
            )

            self.log(f"Generated Card_{i:03}.png")

            self.root.after(
                0,
                lambda i=i: self.status.set(f"Generating Card_{i:03}.png")
            )

        
        self.root.after(
            0,
            lambda: (
                self.status.set("Generation complete"),
                messagebox.showinfo("Done", "Generation complete")
            )
        )

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