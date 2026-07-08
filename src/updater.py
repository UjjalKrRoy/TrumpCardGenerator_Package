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

        temp = tempfile.gettempdir()

        new_exe = os.path.join(
            temp,
            "TrumpCardGenerator_new.exe"
        )

        updater_exe = os.path.join(
            temp,
            "Updater.exe"
        )

        # -----------------------------------------
        # Download new TrumpCardGenerator.exe
        # -----------------------------------------

        response = requests.get(
            GITHUB_EXE,
            stream=True,
            timeout=120
        )

        response.raise_for_status()

        with open(new_exe, "wb") as f:

            for chunk in response.iter_content(8192):

                if chunk:
                    f.write(chunk)

        # -----------------------------------------
        # Download Updater.exe
        # -----------------------------------------

        response = requests.get(
            GITHUB_UPDATER,
            stream=True,
            timeout=120
        )

        response.raise_for_status()

        with open(updater_exe, "wb") as f:

            for chunk in response.iter_content(8192):

                if chunk:
                    f.write(chunk)

        current_exe = sys.executable

        # -----------------------------------------
        # Launch Updater.exe
        # -----------------------------------------

        subprocess.Popen(
            [
                updater_exe,
                new_exe,
                current_exe
            ],
            close_fds=True
        )

        # -----------------------------------------
        # Exit current application
        # -----------------------------------------

        os._exit(0)

    except Exception as e:

        messagebox.showerror(
            "Update",
            f"Unable to download update.\n\n{e}"
        )