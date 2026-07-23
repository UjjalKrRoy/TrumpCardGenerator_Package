import tkinter as tk
from src.gui import CardGeneratorGUI
import ctypes

myappid = "CogniCards.TrumpCardGenerator.1.0"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def main():
    root = tk.Tk()
    app = CardGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()