import os
import sys
import time
import shutil
import subprocess
import tkinter as tk


# --------------------------------------------------------
# Progress Window
# --------------------------------------------------------

root = tk.Tk()

root.title("Trump Card Generator Updater")
root.geometry("420x140")
root.resizable(False, False)

try:
    root.iconbitmap("icon.ico")
except Exception:
    pass

status = tk.StringVar(value="Preparing update...")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill="both", expand=True)

tk.Label(
    frame,
    text="Updating Trump Card Generator",
    font=("Segoe UI", 12, "bold")
).pack(pady=(0, 12))

tk.Label(
    frame,
    textvariable=status,
    font=("Segoe UI", 10)
).pack()


def set_status(text):
    status.set(text)
    root.update()


# --------------------------------------------------------
# Wait until application exits
# --------------------------------------------------------

def wait_for_process(exe_name):

    while True:

        result = subprocess.run(
            f'tasklist /FI "IMAGENAME eq {exe_name}"',
            capture_output=True,
            text=True,
            shell=True
        )

        if exe_name.lower() not in result.stdout.lower():
            break

        set_status("Waiting for application to close...")
        time.sleep(1)


# --------------------------------------------------------
# Main
# --------------------------------------------------------

def main():

    if len(sys.argv) != 3:
        root.destroy()
        sys.exit(1)

    new_exe = sys.argv[1]
    target_exe = sys.argv[2]

    exe_name = os.path.basename(target_exe)

    # Wait until application closes
    wait_for_process(exe_name)

    set_status("Installing update...")

    time.sleep(1)

    success = False

    for _ in range(10):

        try:

            if os.path.exists(target_exe):
                os.remove(target_exe)

            shutil.move(new_exe, target_exe)

            success = True
            break

        except Exception:

            time.sleep(1)

    if not success:

        set_status("Update failed.")

        time.sleep(3)

        root.destroy()

        sys.exit(1)

    set_status("Restarting application...")

    time.sleep(1)

    subprocess.Popen(
        [
            "cmd",
            "/c",
            "start",
            "",
            target_exe
        ],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    root.destroy()


if __name__ == "__main__":

    root.after(100, main)

    root.mainloop()