import os
import re
import threading
import subprocess

# Latest valid distances (meters)
latest_distances = {
    "00:01": None,
    "00:02": None,
    "00:03": None
}

# Current status of anchors
anchor_status = {
    "00:01": False,
    "00:02": False,
    "00:03": False
}


class UWBParser:

    def __init__(self):

        self.current_mac = None
        self.current_status = None

        # Use the SAME Python interpreter as your working environment
        self.cmd = [
            "/home/pi1/uwb_venv/bin/python3",
            "scripts/fira/run_fira_twr/run_fira_twr.py",
            "-p", "/dev/ttyACM0",
            "--session", "1",
            "--node", "onetomany",
            "--mac", "0x0",
            "--dest-mac", "[0x1,0x2,0x3]",
            "--n_controlees", "3",
            "-t", "-1"
        ]

    def start(self):

        t = threading.Thread(target=self.reader)
        t.daemon = True
        t.start()

    def reader(self):

        env = os.environ.copy()

        # Important
        env["PYTHONPATH"] = "/home/pi1/uwb-qorvo-tools"

        process = subprocess.Popen(
            self.cmd,
            cwd="/home/pi1/uwb-qorvo-tools",
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:

            print(line, end="")

            # STATUS
            if "status:" in line.lower():

                if "ok" in line.lower():

                    self.current_status = "OK"

                else:

                    self.current_status = "TIMEOUT"

            # MAC ADDRESS
            elif "mac address:" in line.lower():

                m = re.search(r'([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})', line)

                if m:

                    self.current_mac = m.group(1)

            # DISTANCE
            elif "distance:" in line.lower():

                if self.current_status != "OK":

                    continue

                m = re.search(r'([0-9.]+)\s*cm', line)

                if not m:

                    continue

                if self.current_mac is None:

                    continue

                distance = float(m.group(1)) / 100.0

                latest_distances[self.current_mac] = distance

                anchor_status[self.current_mac] = True


def get_distances():

    return latest_distances


def get_status():

    return anchor_status
