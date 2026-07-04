from pathlib import Path
from PIL import Image, ImageTk

from src.renderer import create_card


class CardPreview:

    def __init__(self, label):
        """
        label = tkinter Label where preview will be displayed.
        """
        self.label = label
        self.photo = None

    def refresh(
        self,
        config,
        template_path,
        font_path,
        question="Sample Question",
        answer="Sample Answer",
    ):
        """
        Regenerates preview image and displays it.
        """

        if template_path is None:
            return

        if font_path is None:
            return

        image = create_card(
            question=question,
            answer=answer,
            output_file=None,
            config=config,
            template_path=template_path,
            font_path=font_path,
            preview=True,
        )

        image.thumbnail((300, 420))

        self.photo = ImageTk.PhotoImage(image)

        self.label.configure(image=self.photo)
        self.label.image = self.photo