import time
import os
import subprocess
import sys
import tempfile
import requests

from tkinter import messagebox

from src.version import APP_VERSION


# --------------------------------------------------------
# GitHub URLs
# --------------------------------------------------------

GITHUB_VERSION = (
    "https://raw.githubusercontent.com/"
    "UjjalKrRoy/TrumpCardGenerator_Package/master/version.json"
)

GITHUB_EXE = (
    "https://github.com/"
    "UjjalKrRoy/TrumpCardGenerator_Package/releases/latest/download/"
    "TrumpCardGenerator.exe"
)

GITHUB_UPDATER = (
    "https://github.com/"
    "UjjalKrRoy/TrumpCardGenerator_Package/releases/latest/download/"
    "Updater.exe"
)


# --------------------------------------------------------
# Version
# --------------------------------------------------------

def get_local_version():
    return APP_VERSION


def get_online_version():

    r = requests.get(GITHUB_VERSION, timeout=15)
    r.raise_for_status()

    return r.json()["version"]


def check_for_update():

    try:

        local = get_local_version()
        online = get_online_version()

        return local != online, online

    except Exception as e:

        messagebox.showerror(
            "Update",
            str(e)
        )

        return False, None


# --------------------------------------------------------
# Download + Replace
# --------------------------------------------------------

def download_and_replace():

    try:

        import tkinter as tk
        from tkinter import ttk

        temp = tempfile.gettempdir()

        new_exe = os.path.join(
            temp,
            "TrumpCardGenerator_new.exe"
        )

        # -----------------------------
        # Download Window
        # -----------------------------

        win = tk.Tk()

        win.title("Trump Card Generator Updater")
        win.geometry("420x180")
        win.resizable(False, False)

        try:
            win.iconbitmap("icon.ico")
        except:
            pass

        ttk.Label(
            win,
            text="Downloading Update",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(15, 8))

        progress = ttk.Progressbar(
            win,
            orient="horizontal",
            length=360,
            mode="determinate"
        )

        progress.pack(pady=10)

        percent = tk.StringVar(value="0 %")

        ttk.Label(
            win,
            textvariable=percent,
            font=("Segoe UI", 10)
        ).pack()

        size_text = tk.StringVar(value="Preparing download...")

        ttk.Label(
            win,
            textvariable=size_text
        ).pack(pady=(8, 0))

        win.update()

        # -----------------------------
        # Download
        # -----------------------------

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

        with open(new_exe, "wb") as f:

            for chunk in response.iter_content(8192):

                if not chunk:
                    continue

                f.write(chunk)

                downloaded += len(chunk)

                if total > 0:

                    p = downloaded * 100 / total

                    progress["value"] = p

                    percent.set(
                        f"{p:.0f} %"
                    )

                    size_text.set(
                        f"{downloaded/1024/1024:.2f} MB / {total/1024/1024:.2f} MB"
                    )

                    win.update()

        # -----------------------------
        # Download Complete
        # -----------------------------

        percent.set("100 %")

        size_text.set(
            "Download Complete"
        )

        progress["value"] = 100

        win.update()

        time.sleep(0.5)

        win.destroy()

        # -----------------------------
        # Start Updater.exe
        # -----------------------------

        current_exe = sys.executable

        updater = os.path.join(
            os.path.dirname(current_exe),
            "Updater.exe"
        )

        subprocess.Popen(
            [
                updater,
                new_exe,
                current_exe
            ]
        )

        os._exit(0)

    except Exception as e:

        messagebox.showerror(
            "Update",
            f"Unable to download update.\n\n{e}"
        )