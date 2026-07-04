import tkinter as tk
from src.gui import CardGeneratorGUI


def main():
    root = tk.Tk()
    app = CardGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()