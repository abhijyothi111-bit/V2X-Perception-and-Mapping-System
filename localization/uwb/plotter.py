import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

from config import ANCHORS
from parser import get_distances, get_status
from trilateration import trilaterate


class Plotter:

    def __init__(self):

        self.fig, self.ax = plt.subplots(figsize=(7,7))

    def update(self, frame):

        self.ax.clear()

        self.ax.set_title("UWB Localization")

        self.ax.set_xlabel("X (m)")
        self.ax.set_ylabel("Y (m)")

        self.ax.set_xlim(-2,6)
        self.ax.set_ylim(-1,7)

        self.ax.grid(True)

        distances = get_distances()
        status = get_status()

        # Draw Anchors
        for mac,(x,y) in ANCHORS.items():

            self.ax.scatter(x,y,color="blue",s=100)

            self.ax.text(
                x,
                y+0.15,
                mac,
                fontsize=10
            )

        valid=[]

        # Draw circles for available anchors
        for mac in ANCHORS:

            if status[mac]:

                x,y=ANCHORS[mac]

                r=distances[mac]

                circle=Circle(
                    (x,y),
                    r,
                    fill=False,
                    linewidth=2
                )

                self.ax.add_patch(circle)

                valid.append(mac)

        # No anchors
        if len(valid)==0:

            self.ax.text(
                1,
                6,
                "Waiting for ranging...",
                fontsize=12,
                color="red"
            )

            return

        # One or Two anchors
        if len(valid)<3:

            return

        anchors=[
            ANCHORS["00:01"],
            ANCHORS["00:02"],
            ANCHORS["00:03"]
        ]

        d=[
            distances["00:01"],
            distances["00:02"],
            distances["00:03"]
        ]

        pos=trilaterate(
            anchors,
            d
        )

        if pos is None:

            return

        x=float(pos[0])
        y=float(pos[1])

        self.ax.scatter(
            x,
            y,
            color="red",
            s=180
        )

        self.ax.text(
            x,
            y+0.2,
            "TAG"
        )

        self.ax.text(
            -1.8,
            6.5,
            f"X={x:.2f} m\nY={y:.2f} m",
            fontsize=10
        )

    def start(self):

        self.anim(
            self.fig,
            self.update,
            interval=200,
            cache_frame_data=False
        )

        plt.show()
