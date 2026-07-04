import ctypes
import tkinter as tk
from src.gui import CardGeneratorGUI


def main():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    root = tk.Tk()
    CardGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()