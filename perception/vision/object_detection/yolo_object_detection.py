import cv2
import socket
import json
import time
from ultralytics import YOLO

# ==========================
# Configuration
# ==========================
JETSON_IP = "192.168.0.100"
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam")
    exit()

prev_time = time.time()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, verbose=False)

    annotated = results[0].plot()

    detections = []

    for box in results[0].boxes:

        cls = int(box.cls[0])
        conf = float(box.conf[0])

        x1, y1, x2, y2 = box.xyxy[0]

        detections.append({

            "object": model.names[cls],

            "confidence": round(conf, 2),

            "bbox": [
                int(x1),
                int(y1),
                int(x2),
                int(y2)
            ]
        })

    packet = {

        "device": "Vehicle_1",

        "time": time.strftime("%H:%M:%S"),

        "objects": detections

    }

    sock.sendto(json.dumps(packet).encode(), (JETSON_IP, PORT))

    fps = 1/(time.time()-prev_time)
    prev_time = time.time()

    cv2.putText(
        annotated,
        f"FPS : {int(fps)}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow("Vehicle A - YOLO Detection", annotated)

    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
sock.close()
