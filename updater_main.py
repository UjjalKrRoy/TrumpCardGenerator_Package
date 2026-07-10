import os
import sys
import time
import shutil
import tempfile
import subprocess
import requests

import tkinter as tk
from tkinter import ttk, messagebox


# --------------------------------------------------------
# GitHub
# --------------------------------------------------------

GITHUB_EXE = (
    "https://github.com/"
    "UjjalKrRoy/TrumpCardGenerator_Package/releases/latest/download/"
    "TrumpCardGenerator.exe"
)


# --------------------------------------------------------
# Tk Window
# --------------------------------------------------------

root = tk.Tk()

root.title("Trump Card Generator Updater")
root.geometry("520x300")
root.resizable(False, False)

try:
    root.iconbitmap("icon.ico")
except:
    pass


# --------------------------------------------------------
# Header
# --------------------------------------------------------

title = tk.StringVar(
    value="Updating Trump Card Generator"
)

tk.Label(
    root,
    textvariable=title,
    font=("Segoe UI", 13, "bold")
).pack(
    pady=(15, 10)
)


# --------------------------------------------------------
# Progress
# --------------------------------------------------------

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    mode="determinate",
    length=460
)

progress.pack(
    pady=(5, 5)
)

percent = tk.StringVar(
    value="0 %"
)

tk.Label(
    root,
    textvariable=percent,
    font=("Segoe UI", 10)
).pack()


# --------------------------------------------------------
# Current Status
# --------------------------------------------------------

status = tk.StringVar(
    value="Preparing..."
)

tk.Label(
    root,
    textvariable=status,
    font=("Segoe UI", 10)
).pack(
    pady=(8, 12)
)


# --------------------------------------------------------
# Checklist
# --------------------------------------------------------

download_state = tk.StringVar(
    value="⬜ Downloading update..."
)

wait_state = tk.StringVar(
    value="⬜ Waiting for application to close..."
)

install_state = tk.StringVar(
    value="⬜ Installing update..."
)

cleanup_state = tk.StringVar(
    value="⬜ Cleaning temporary files..."
)

restart_state = tk.StringVar(
    value="⬜ Restarting application..."
)


for item in (
    download_state,
    wait_state,
    install_state,
    cleanup_state,
    restart_state
):

    tk.Label(
        root,
        textvariable=item,
        anchor="w",
        justify="left",
        font=("Segoe UI", 9)
    ).pack(
        fill="x",
        padx=25,
        pady=2
    )


# --------------------------------------------------------
# Helper Functions
# --------------------------------------------------------

def update_progress(value):

    progress["value"] = value

    percent.set(f"{value:.0f} %")

    root.update()


def update_status(text):

    status.set(text)

    root.update()


def complete(item, text):

    item.set(f"✔ {text}")

    root.update()


def working(item, text):

    item.set(f"⏳ {text}")

    root.update()


def failed(item, text):

    item.set(f"❌ {text}")

    root.update()


# --------------------------------------------------------
# Temporary Files
# --------------------------------------------------------

TEMP = tempfile.gettempdir()

NEW_EXE = os.path.join(
    TEMP,
    "TrumpCardGenerator_new.exe"
)

TARGET_EXE = os.path.abspath(
    sys.argv[1]
)
# --------------------------------------------------------
# Download Latest EXE
# --------------------------------------------------------

def download_latest_exe():

    working(
        download_state,
        "Downloading update..."
    )

    update_status(
        "Downloading latest version..."
    )

    response = requests.get(
        GITHUB_EXE,
        stream=True,
        timeout=120
    )

    response.raise_for_status()

    total = int(
        response.headers.get(
            "content-length",
            0
        )
    )

    downloaded = 0

    with open(
        NEW_EXE,
        "wb"
    ) as f:

        for chunk in response.iter_content(8192):

            if not chunk:
                continue

            f.write(chunk)

            downloaded += len(chunk)

            if total > 0:

                percent_value = downloaded * 100 / total

                update_progress(
                    percent_value
                )

                status.set(
                    f"Downloading "
                    f"{downloaded/1024/1024:.2f} MB / "
                    f"{total/1024/1024:.2f} MB"
                )

                root.update()

    update_progress(100)

    complete(
        download_state,
        "Downloading update..."
    )

    update_status(
        "Download complete."
    )

    time.sleep(0.5)


# --------------------------------------------------------
# Wait Until App Closes
# --------------------------------------------------------

def wait_for_process():

    exe_name = os.path.basename(
        TARGET_EXE
    )

    working(
        wait_state,
        "Waiting for application to close..."
    )

    update_status(
        "Waiting for application..."
    )

    while True:

        result = subprocess.run(
            f'tasklist /FI "IMAGENAME eq {exe_name}"',
            capture_output=True,
            text=True,
            shell=True
        )

        if exe_name.lower() not in result.stdout.lower():

            break

        root.update()

        time.sleep(1)

    complete(
        wait_state,
        "Waiting for application to close..."
    )
# --------------------------------------------------------
# Install Update
# --------------------------------------------------------

def install_update():

    working(
        install_state,
        "Installing update..."
    )

    update_status(
        "Installing update..."
    )

    success = False

    for _ in range(10):

        try:

            if os.path.exists(TARGET_EXE):
                os.remove(TARGET_EXE)

            shutil.move(
                NEW_EXE,
                TARGET_EXE
            )

            success = True

            break

        except Exception:

            time.sleep(1)

    if not success:

        failed(
            install_state,
            "Installing update..."
        )

        raise RuntimeError(
            "Unable to replace application."
        )

    complete(
        install_state,
        "Installing update..."
    )


# --------------------------------------------------------
# Cleanup
# --------------------------------------------------------

def cleanup():

    working(
        cleanup_state,
        "Cleaning temporary files..."
    )

    update_status(
        "Cleaning temporary files..."
    )

    try:

        if os.path.exists(NEW_EXE):
            os.remove(NEW_EXE)

    except:
        pass

    complete(
        cleanup_state,
        "Cleaning temporary files..."
    )


# --------------------------------------------------------
# Restart Application
# --------------------------------------------------------

def restart_application():

    working(
        restart_state,
        "Restarting application..."
    )

    update_status(
        "Launching application..."
    )

    subprocess.Popen(
        [
            "cmd",
            "/c",
            "start",
            "",
            TARGET_EXE
        ],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    complete(
        restart_state,
        "Restarting application..."
    )

    update_progress(100)

    update_status(
        "Update completed successfully."
    )

    time.sleep(2)


# --------------------------------------------------------
# Main
# --------------------------------------------------------

def main():

    try:

        if len(sys.argv) != 2:

            raise RuntimeError(
                "Target executable not supplied."
            )

        download_latest_exe()

        wait_for_process()

        install_update()

        cleanup()

        restart_application()

        root.destroy()

    except Exception as e:

        messagebox.showerror(
            "Update Failed",
            str(e)
        )

        root.destroy()


# --------------------------------------------------------
# Entry
# --------------------------------------------------------

if __name__ == "__main__":

    root.after(
        200,
        main
    )

    root.mainloop()