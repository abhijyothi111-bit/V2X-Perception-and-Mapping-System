# config.py

# Anchor coordinates (meters)
ANCHORS = {
    "00:01": (0.0, 1.0),
    "00:02": (0.0, 5.0),
    "00:03": (2.5, 3.0)
}

# Update interval
UPDATE_RATE = 0.2

# Ignore impossible ranges
MIN_DISTANCE = 0.20
MAX_DISTANCE = 20.0

# Exponential Moving Average filter
ALPHA = 0.35

# Keep last valid distances
LAST_DISTANCE = {
    "00:01": None,
    "00:02": None,
    "00:03": None
}
