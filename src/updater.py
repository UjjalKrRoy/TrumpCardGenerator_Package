import json
import os
import subprocess
import sys
import tempfile
import requests

from tkinter import messagebox

GITHUB_VERSION = "https://raw.githubusercontent.com/UjjalKrRoy/TrumpCardGenerator_Package/master/version.json"

GITHUB_EXE = "https://github.com/UjjalKrRoy/TrumpCardGenerator_Package/releases/latest/download/TrumpCardGenerator.exe"


def get_local_version():

    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.dirname(__file__))

    version_file = os.path.join(base, "version.json")

    with open(version_file, "r") as f:
        return json.load(f)["version"]


def get_online_version():

    r = requests.get(GITHUB_VERSION, timeout=10)

    r.raise_for_status()

    return r.json()["version"]


def check_for_update():

    try:

        local = get_local_version()

        online = get_online_version()

        return online != local, online

    except Exception as e:

        messagebox.showerror(
            "Update",
            str(e)
        )

        return False, None


def download_and_replace():

    try:

        temp = tempfile.gettempdir()

        new_exe = os.path.join(
            temp,
            "TrumpCardGenerator_new.exe"
        )

        r = requests.get(
            GITHUB_EXE,
            stream=True,
            timeout=60
        )

        r.raise_for_status()

        with open(new_exe, "wb") as f:

            for chunk in r.iter_content(8192):

                f.write(chunk)

        current = sys.executable

        bat = os.path.join(
            temp,
            "update.bat"
        )

        with open(bat, "w") as b:

            b.write(f"""@echo off
timeout /t 2 >nul

:loop
tasklist | find /I "TrumpCardGenerator.exe" >nul
if not errorlevel 1 (
    timeout /t 1 >nul
    goto loop
)

copy /Y "{new_exe}" "{current}"

start "" "{current}"

del "{new_exe}"

del "%~f0"
""")

        subprocess.Popen(
            bat,
            shell=True
        )

        sys.exit()

    except Exception as e:

        messagebox.showerror(
            "Update",
            f"Unable to download update.\n\n{e}"
        )