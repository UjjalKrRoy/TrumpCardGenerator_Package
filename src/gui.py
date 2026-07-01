import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext

from openpyxl import load_workbook

from src.config import load_config
from src.renderer import create_card


class CardGeneratorGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Trump Card Generator")
        self.root.geometry("800x650")
        self.root.resizable(False, False)

        # -------------------------------
        # Variables
        # -------------------------------
        self.template_path = None
        self.font_path = None
        self.excel_path = None
        self.output_dir = None

        # -------------------------------
        # Title
        # -------------------------------
        title = tk.Label(
            root,
            text="Trump Card Generator",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        # -------------------------------
        # Main Frame
        # -------------------------------
        frame = tk.Frame(root)
        frame.pack(fill="x", padx=15)

        # ===============================
        # Template
        # ===============================
        tk.Label(frame, text="Front Image", width=15, anchor="w").grid(
            row=0, column=0, pady=5
        )

        self.lbl_template = tk.Label(
            frame,
            text="Not Selected",
            width=50,
            anchor="w",
            relief="sunken"
        )
        self.lbl_template.grid(row=0, column=1, padx=5)

        tk.Button(
            frame,
            text="Browse",
            command=self.select_template
        ).grid(row=0, column=2)

        # ===============================
        # Font
        # ===============================
        tk.Label(frame, text="Font", width=15, anchor="w").grid(
            row=1, column=0, pady=5
        )

        self.lbl_font = tk.Label(
            frame,
            text="Not Selected",
            width=50,
            anchor="w",
            relief="sunken"
        )
        self.lbl_font.grid(row=1, column=1, padx=5)

        tk.Button(
            frame,
            text="Browse",
            command=self.select_font
        ).grid(row=1, column=2)

        # ===============================
        # Excel
        # ===============================
        tk.Label(frame, text="Excel File", width=15, anchor="w").grid(
            row=2, column=0, pady=5
        )

        self.lbl_excel = tk.Label(
            frame,
            text="Not Selected",
            width=50,
            anchor="w",
            relief="sunken"
        )
        self.lbl_excel.grid(row=2, column=1, padx=5)

        tk.Button(
            frame,
            text="Browse",
            command=self.select_excel
        ).grid(row=2, column=2)

        # ===============================
        # Output Folder
        # ===============================
        tk.Label(frame, text="Output Folder", width=15, anchor="w").grid(
            row=3, column=0, pady=5
        )

        self.lbl_output = tk.Label(
            frame,
            text="Not Selected",
            width=50,
            anchor="w",
            relief="sunken"
        )
        self.lbl_output.grid(row=3, column=1, padx=5)

        tk.Button(
            frame,
            text="Browse",
            command=self.select_output
        ).grid(row=3, column=2)

        # ===============================
        # Generate Button
        # ===============================
        self.btn_generate = tk.Button(
            root,
            text="Generate Cards",
            bg="green",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.start_generation
        )

        self.btn_generate.pack(pady=15)

        # ===============================
        # Log Window
        # ===============================
        self.log_box = scrolledtext.ScrolledText(
            root,
            width=95,
            height=22
        )

        self.log_box.pack(padx=10, pady=10)

    # =====================================================
    # Logging
    # =====================================================

    def log(self, message):
        self.root.after(0, lambda: self._append_log(message))

    def _append_log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    # =====================================================
    # Browse Buttons
    # =====================================================

    def select_template(self):

        file = filedialog.askopenfilename(

            title="Select Front Image",

            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg")
            ]
        )

        if file:
            self.template_path = Path(file)
            self.lbl_template.config(text=self.template_path.name)
            self.log(f"🖼 Template : {self.template_path}")

    def select_font(self):

        file = filedialog.askopenfilename(

            title="Select Font",

            filetypes=[
                ("TrueType Font", "*.ttf")
            ]
        )

        if file:
            self.font_path = Path(file)
            self.lbl_font.config(text=self.font_path.name)
            self.log(f"🔤 Font : {self.font_path}")

    def select_excel(self):

        file = filedialog.askopenfilename(

            title="Select Excel File",

            filetypes=[
                ("Excel Files", "*.xlsx")
            ]
        )

        if file:
            self.excel_path = Path(file)
            self.lbl_excel.config(text=self.excel_path.name)
            self.log(f"📄 Excel : {self.excel_path}")

    def select_output(self):

        folder = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if folder:
            self.output_dir = Path(folder)
            self.lbl_output.config(text=str(self.output_dir))
            self.log(f"📁 Output : {self.output_dir}")

    # =====================================================
    # Generate
    # =====================================================

    def start_generation(self):

        if not self.template_path:
            messagebox.showerror("Error", "Please select Front Image.")
            return

        if not self.font_path:
            messagebox.showerror("Error", "Please select Font.")
            return

        if not self.excel_path:
            messagebox.showerror("Error", "Please select Excel file.")
            return

        if not self.output_dir:
            messagebox.showerror("Error", "Please select Output folder.")
            return

        self.btn_generate.config(state=tk.DISABLED)

        thread = threading.Thread(
            target=self.generate_cards,
            daemon=True
        )

        thread.start()

    # =====================================================
    # Main Generation
    # =====================================================

    def generate_cards(self):

        try:

            base_dir = Path(__file__).resolve().parent.parent

            config = load_config(
                base_dir / "config.json"
            )

            wb = load_workbook(self.excel_path)
            ws = wb.active

            self.output_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            self.log("")
            self.log("===================================")
            self.log("Starting Card Generation")
            self.log("===================================")

            count = 0

            for index, row in enumerate(
                    ws.iter_rows(min_row=2, values_only=True),
                    start=1):

                if not row:
                    continue

                if row[0] is None or row[1] is None:
                    self.log(f"⚠ Skipping row {index}")
                    continue

                question = str(row[0]).strip()
                answer = str(row[1]).strip()

                output_file = (
                    self.output_dir /
                    f"Card_{index:03}.png"
                )

                create_card(
                    question=question,
                    answer=answer,
                    output_file=output_file,
                    config=config,
                    template_path=self.template_path,
                    font_path=self.font_path
                )

                count += 1

                self.log(
                    f"✅ Generated : {output_file.name}"
                )

            self.log("")
            self.log(f"🎉 Successfully generated {count} cards.")

            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Completed",
                    f"{count} cards generated successfully."
                )
            )

        except Exception as e:

            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Error",
                    str(e)
                )
            )

            self.log(f"❌ {e}")

        finally:

            self.root.after(
                0,
                lambda: self.btn_generate.config(
                    state=tk.NORMAL
                )
            )


if __name__ == "__main__":

    root = tk.Tk()

    CardGeneratorGUI(root)

    root.mainloop()