import subprocess
import sys
import tempfile
import os
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

        current_exe = sys.executable

        bat_file = os.path.join(
            temp,
            "TrumpCardGenerator_Update.bat"
        )

        with open(bat_file, "w") as f:

            f.write(f"""@echo off
setlocal

echo Waiting for application to close...

:WAIT
tasklist /FI "IMAGENAME eq TrumpCardGenerator.exe" | find /I "TrumpCardGenerator.exe" >nul
if not errorlevel 1 (
    timeout /t 1 >nul
    goto WAIT
)

echo Replacing executable...

move /Y "{new_exe}" "{current_exe}" >nul

if errorlevel 1 (
    copy /Y "{new_exe}" "{current_exe}" >nul
)

timeout /t 3 >nul

start "" "{current_exe}"

del "{new_exe}" >nul 2>&1

del "%~f0"
""")

        subprocess.Popen(
            ["cmd", "/c", bat_file],
            creationflags=subprocess.CREATE_NO_WINDOW,
            close_fds=True
        )

        # Exit immediately
        os._exit(0)

    except Exception as e:

        messagebox.showerror(
            "Update",
            f"Unable to download update.\n\n{e}"
        )