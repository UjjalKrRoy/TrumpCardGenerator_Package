from pathlib import Path
from openpyxl import load_workbook

from src.renderer import create_card


class CardGenerator:
    """
    Batch card generator from Excel.
    Works with MS Word-style font system (font family or system font path).
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
        self.font_path = font_path  # can be font family OR resolved path
        self.excel_path = Path(excel_path)
        self.output_dir = Path(output_dir)
        self.logger = logger

    # -------------------------------------------------
    # Logging helper
    # -------------------------------------------------
    def log(self, message):
        if self.logger:
            self.logger(message)

    # -------------------------------------------------
    # Main generation
    # -------------------------------------------------
    def generate(self):
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")

        if not self.excel_path.exists():
            raise FileNotFoundError(f"Excel file not found: {self.excel_path}")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        workbook = load_workbook(self.excel_path)
        sheet = workbook.active

        generated = 0

        # -------------------------------------------------
        # Iterate Excel rows (skip header)
        # -------------------------------------------------
        for row_index, row in enumerate(
            sheet.iter_rows(min_row=2, values_only=True),
            start=1
        ):
            if not row:
                continue

            question = row[0]
            answer = row[1]

            # Skip invalid rows safely
            if not question or not answer:
                self.log(f"Skipping row {row_index} (missing data)")
                continue

            output_file = self.output_dir / f"Card_{row_index:03}.png"

            try:
                create_card(
                    question=str(question),
                    answer=str(answer),
                    output_file=output_file,
                    config=self.config,
                    template_path=self.template_path,
                    font_path=self.font_path,  # MS Word-style font input
                )

                generated += 1
                self.log(f"Generated {output_file.name}")

            except Exception as e:
                self.log(f"Error in row {row_index}: {e}")

        self.log(f"\nFinished: {generated} cards generated")

        return generated