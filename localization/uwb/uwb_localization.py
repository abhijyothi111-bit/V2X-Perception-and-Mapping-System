#!/usr/bin/env python3

import subprocess
import threading
import re
import numpy as np
import os

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# -------------------------------------------------
# CHANGE THESE IF YOUR ANCHOR POSITIONS CHANGE
# -------------------------------------------------

ANCHORS = {
    "00:01": (0.0, 1.0),
    "00:02": (0.0, 5.0),
    "00:03": (2.5, 3.0),
}

# Latest valid distance for every anchor
DISTANCES = {
    "00:01": None,
    "00:02": None,
    "00:03": None,
}

# -------------------------------------------------
# YOUR NORMAL QORVO COMMAND
# -------------------------------------------------

CMD = [
    "bash",
    "-c",
    'source ~/uwb_venv/bin/activate && '
    'cd ~/uwb-qorvo-tools && '
    'python3 scripts/fira/run_fira_twr/run_fira_twr.py '
    '-p /dev/ttyACM0 '
    '--node onetomany '
    '--mac 0x0 '
    '--dest-mac "[0x1,0x2,0x3]" '
    '--n_controlees 3 '
    '-t -1'
]

current_status = None
current_mac = None

fig, ax = plt.subplots(figsize=(7,7))

tag_x = None
tag_y = None


def trilaterate(anchor_pos, dist):

    x1,y1 = anchor_pos[0]
    x2,y2 = anchor_pos[1]
    x3,y3 = anchor_pos[2]

    r1,r2,r3 = dist

    A = np.array([
        [2*(x2-x1),2*(y2-y1)],
        [2*(x3-x1),2*(y3-y1)]
    ])

    B = np.array([
        r1*r1-r2*r2-x1*x1+x2*x2-y1*y1+y2*y2,
        r1*r1-r3*r3-x1*x1+x3*x3-y1*y1+y3*y3
    ])

    try:
        return np.linalg.solve(A,B)

    except:
        return None
    
    
def reader():

    global current_status
    global current_mac
    global tag_x
    global tag_y

    process = subprocess.Popen(
    CMD,
    executable="/bin/bash",
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

    for line in process.stdout:

        print(line, end="")

        line_lower = line.lower()

        # ----------------------------
        # STATUS
        # ----------------------------
        if "status:" in line_lower:

            if "ok" in line_lower:
                current_status = True
            else:
                current_status = False

        # ----------------------------
        # MAC ADDRESS
        # ----------------------------
        elif "mac address:" in line_lower:

            m = re.search(r'([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})', line)

            if m:
                current_mac = m.group(1)

        # ----------------------------
        # DISTANCE
        # ----------------------------
        elif "distance:" in line_lower:

            if current_status is False:
                continue

            m = re.search(r'([0-9.]+)\s*cm', line)

            if not m:
                continue

            if current_mac not in DISTANCES:
                continue

            d = float(m.group(1))/100.0

            DISTANCES[current_mac] = d

            if all(v is not None for v in DISTANCES.values()):

                pos = trilaterate(
                    [
                        ANCHORS["00:01"],
                        ANCHORS["00:02"],
                        ANCHORS["00:03"]
                    ],
                    [
                        DISTANCES["00:01"],
                        DISTANCES["00:02"],
                        DISTANCES["00:03"]
                    ]
                )

                if pos is not None:

                    tag_x = float(pos[0])
                    tag_y = float(pos[1])
                    
                    
def update(frame):

    ax.clear()

    ax.set_title("UWB Live Localization")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")

    ax.set_xlim(-2,6)
    ax.set_ylim(-1,7)

    ax.grid(True)

    # Draw anchors
    for mac,(x,y) in ANCHORS.items():

        ax.scatter(x,y,color="blue",s=120)

        ax.text(
            x,
            y+0.15,
            mac,
            fontsize=10
        )

        # Draw ranging circle if available
        if DISTANCES[mac] is not None:

            circle = Circle(
                (x,y),
                DISTANCES[mac],
                fill=False,
                linewidth=2
            )

            ax.add_patch(circle)

    # Draw tag if trilateration succeeded
    if tag_x is not None:

        ax.scatter(
            tag_x,
            tag_y,
            color="red",
            s=180
        )

        ax.text(
            tag_x,
            tag_y+0.15,
            "TAG",
            fontsize=12
        )

        ax.text(
            -1.8,
            6.4,
            f"X = {tag_x:.2f} m\nY = {tag_y:.2f} m",
            fontsize=11
        )

    else:

        ax.text(
            -1.8,
            6.4,
            "Waiting for 3 valid ranges...",
            fontsize=11,
            color="red"
        )


# ------------------------------
# Start Qorvo Reader
# ------------------------------

thread = threading.Thread(
    target=reader,
    daemon=True
)

thread.start()

ani = FuncAnimation(
    fig,
    update,
    interval=200,
    cache_frame_data=False
)

plt.show()
