import os
import sys
import shutil
import uuid
import subprocess
import requests

from tkinter import messagebox

from src.version import APP_VERSION


# --------------------------------------------------------
# GitHub Version URL
# --------------------------------------------------------

GITHUB_VERSION = (
    "https://raw.githubusercontent.com/"
    "UjjalKrRoy/TrumpCardGenerator_Package/master/version.json"
)


# --------------------------------------------------------
# Version
# --------------------------------------------------------

def get_local_version():

    return APP_VERSION


def get_online_version():

    r = requests.get(
        GITHUB_VERSION,
        timeout=15
    )

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
# Extract embedded Updater.exe
# --------------------------------------------------------

def extract_updater():

    import tempfile

    temp = tempfile.gettempdir()

    updater = os.path.join(
        temp,
        f"Updater_{uuid.uuid4().hex}.exe"
    )

    if getattr(sys, "frozen", False):

        source = os.path.join(
            sys._MEIPASS,
            "Updater.exe"
        )

    else:

        source = os.path.join(
            os.getcwd(),
            "dist",
            "Updater.exe"
        )

    if not os.path.exists(source):

        raise FileNotFoundError(
            f"Embedded Updater.exe not found:\n{source}"
        )

    shutil.copy2(
        source,
        updater
    )

    return updater


# --------------------------------------------------------
# Launch Updater
# --------------------------------------------------------

def download_and_replace():

    try:

        updater = extract_updater()

        current_exe = os.path.abspath(
            sys.executable
        )

        subprocess.Popen(
            [
                updater,
                current_exe
            ],
            close_fds=True
        )

        os._exit(0)

    except Exception as e:

        messagebox.showerror(
            "Update",
            f"Unable to start updater.\n\n{e}"
        )