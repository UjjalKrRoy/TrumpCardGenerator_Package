import traceback
import os
import sys
import time
import tempfile
import subprocess
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

    except Exception:

        messagebox.showerror(
            "Update Error",
            traceback.format_exc()
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

        updater_exe = os.path.join(
            temp,
            "Updater.exe"
        )

        # --------------------------------------------------
        # Progress Window
        # --------------------------------------------------

        win = tk.Tk()

        win.title("Trump Card Generator Updater")
        win.geometry("430x180")
        win.resizable(False, False)

        try:
            win.iconbitmap("icon.ico")
        except:
            pass

        ttk.Label(
            win,
            text="Downloading Update",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(15, 10))

        progress = ttk.Progressbar(
            win,
            orient="horizontal",
            length=360,
            mode="determinate"
        )

        progress.pack()

        percent = tk.StringVar(value="0 %")

        ttk.Label(
            win,
            textvariable=percent
        ).pack(pady=(8, 0))

        status = tk.StringVar(value="Preparing download...")

        ttk.Label(
            win,
            textvariable=status
        ).pack(pady=(5, 0))

        win.update()

        # --------------------------------------------------
        # Download Main EXE
        # --------------------------------------------------

        response = requests.get(
            GITHUB_EXE,
            stream=True,
            timeout=120
        )

        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))

        downloaded = 0

        with open(new_exe, "wb") as f:

            for chunk in response.iter_content(8192):

                if not chunk:
                    continue

                f.write(chunk)

                downloaded += len(chunk)

                if total:

                    p = downloaded * 100 / total

                    progress["value"] = p

                    percent.set(f"{p:.0f} %")

                    status.set(
                        f"Downloading application ({downloaded//1024//1024} MB / {total//1024//1024} MB)"
                    )

                    win.update()

        # --------------------------------------------------
        # Download Updater.exe
        # --------------------------------------------------

        progress["value"] = 0
        percent.set("0 %")
        status.set("Downloading updater...")

        win.update()

        response = requests.get(
            GITHUB_UPDATER,
            stream=True,
            timeout=60
        )

        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))

        downloaded = 0

        with open(updater_exe, "wb") as f:

            for chunk in response.iter_content(8192):

                if not chunk:
                    continue

                f.write(chunk)

                downloaded += len(chunk)

                if total:

                    p = downloaded * 100 / total

                    progress["value"] = p

                    percent.set(f"{p:.0f} %")

                    win.update()

        progress["value"] = 100
        percent.set("100 %")
        status.set("Starting updater...")

        win.update()

        time.sleep(0.7)

        win.destroy()

        # --------------------------------------------------
        # Start updater
        # --------------------------------------------------

        current_exe = os.path.abspath(sys.executable)

        messagebox.showinfo(
            "Updater Debug",
            f"""
        Updater.exe
        {updater_exe}

        Exists:
        {os.path.exists(updater_exe)}

        Downloaded EXE
        {new_exe}

        Exists:
        {os.path.exists(new_exe)}

        Current EXE
        {current_exe}

        Exists:
        {os.path.exists(current_exe)}
        """
        )

        # Wait until Windows finishes writing Updater.exe
        for _ in range(20):

            if os.path.exists(updater_exe):
                break

            time.sleep(0.25)

        # Small delay to avoid WinError 2
        time.sleep(1)

        subprocess.Popen(
            [
                updater_exe,
                new_exe,
                current_exe
            ],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        os._exit(0)

    except Exception:

        messagebox.showerror(
            "Update Error",
            traceback.format_exc()
        )