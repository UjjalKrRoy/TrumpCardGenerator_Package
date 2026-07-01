from pathlib import Path
from openpyxl import load_workbook

from src.renderer import create_card


class CardGenerator:
    """
    Batch generator for card images from Excel file.

    Works with:
    - MS Word-style fonts (family name or system path)
    - Config-driven layout
    - GUI or CLI logging
    """

    def __init__(
        self,
        config,
        template_path,
        font_path,
        excel_path,
        output_dir,
        logger=None,
    ):
        self.config = config
        self.template_path = Path(template_path)
        self.font_path = font_path
        self.excel_path = Path(excel_path)
        self.output_dir = Path(output_dir)
        self.logger = logger

    # -------------------------------------------------
    # Logger helper
    # -------------------------------------------------
    def log(self, msg):
        if self.logger:
            self.logger(msg)

    # -------------------------------------------------
    # MAIN GENERATION FUNCTION
    # -------------------------------------------------
    def generate(self):
        # Validate inputs
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")

        if not self.excel_path.exists():
            raise FileNotFoundError(f"Excel file not found: {self.excel_path}")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        workbook = load_workbook(self.excel_path)
        sheet = workbook.active

        generated = 0
        skipped = 0

        # -------------------------------------------------
        # Iterate rows (skip header row)
        # -------------------------------------------------
        for row_index, row in enumerate(
            sheet.iter_rows(min_row=2, values_only=True),
            start=1
        ):
            # Safe row check
            if not row or len(row) < 2:
                self.log(f"Skipping row {row_index} (invalid structure)")
                skipped += 1
                continue

            question = row[0]
            answer = row[1]

            # Skip empty data
            if not question or not answer:
                self.log(f"Skipping row {row_index} (missing data)")
                skipped += 1
                continue

            output_file = self.output_dir / f"Card_{row_index:03}.png"

            try:
                create_card(
                    question=str(question).strip(),
                    answer=str(answer).strip(),
                    output_file=output_file,
                    config=self.config,
                    template_path=self.template_path,
                    font_path=self.font_path,
                )

                generated += 1
                self.log(f"Generated: {output_file.name}")

            except Exception as e:
                self.log(f"Error row {row_index}: {e}")
                skipped += 1

        # Final summary
        self.log(f"\nDone → Generated: {generated}, Skipped: {skipped}")

        return generated