import os
import sys
import time
import shutil
import subprocess


def wait_for_process(exe_name):
    """
    Wait until the application has completely exited.
    """

    while True:

        result = subprocess.run(
            'tasklist /FI "IMAGENAME eq {}"'.format(exe_name),
            capture_output=True,
            text=True,
            shell=True
        )

        if exe_name.lower() not in result.stdout.lower():
            break

        time.sleep(1)


def main():

    if len(sys.argv) != 3:
        sys.exit(1)

    new_exe = sys.argv[1]
    target_exe = sys.argv[2]

    exe_name = os.path.basename(target_exe)

    # Wait until the application has exited
    wait_for_process(exe_name)

    # Give Windows a little extra time
    time.sleep(2)

    # Try replacing several times
    for _ in range(10):

        try:

            if os.path.exists(target_exe):
                os.remove(target_exe)

            shutil.move(new_exe, target_exe)

            break

        except Exception:

            time.sleep(1)

    # Small delay before restarting
    time.sleep(2)

    subprocess.Popen(
        [target_exe],
        close_fds=True
    )

    # Delete downloaded file if still exists
    try:

        if os.path.exists(new_exe):
            os.remove(new_exe)

    except:
        pass


if __name__ == "__main__":
    main()