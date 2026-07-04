from tkinter import filedialog, messagebox


def select_image():

    return filedialog.askopenfilename(
        filetypes=[
            ("Images", "*.png *.jpg *.jpeg")
        ]
    )


def select_excel():

    return filedialog.askopenfilename(
        filetypes=[
            ("Excel", "*.xlsx")
        ]
    )


def select_output():

    return filedialog.askdirectory()


def error(msg):

    messagebox.showerror("Error", msg)


def info(msg):

    messagebox.showinfo("Done", msg)