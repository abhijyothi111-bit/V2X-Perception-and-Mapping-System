# trilateration.py

import numpy as np

def trilaterate(anchors, distances):
    """
    anchors: list of (x,y)
    distances: list of distances in meters

    Returns:
        (x,y) or None
    """

    if len(anchors) != 3 or len(distances) != 3:
        return None

    try:
        (x1, y1), (x2, y2), (x3, y3) = anchors
        d1, d2, d3 = distances

        A = np.array([
            [2*(x2-x1), 2*(y2-y1)],
            [2*(x3-x1), 2*(y3-y1)]
        ])

        B = np.array([
            d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2,
            d1**2 - d3**2 - x1**2 + x3**2 - y1**2 + y3**2
        ])

        position = np.linalg.solve(A, B)

        return position[0], position[1]

    except Exception:
        return None
