from ultralytics import YOLO
import cv2
import socket
import json
import argparse
from datetime import datetime


def main():

    # ---------------------------------------------------------
    # Command-line arguments
    # ---------------------------------------------------------

    parser = argparse.ArgumentParser(
        description="YOLO Object and Accident Detection"
    )

    parser.add_argument(
        "--model",
        required=True,
        help="Path to trained YOLO model (.pt)"
    )

    parser.add_argument(
        "--video",
        required=True,
        help="Path to input video"
    )

    parser.add_argument(
        "--receiver",
        default="192.168.0.100",
        help="Receiver / Jetson IP address"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="UDP port"
    )

    args = parser.parse_args()

    # ---------------------------------------------------------
    # Load trained YOLO model
    # ---------------------------------------------------------

    print("Loading YOLO model...")

    model = YOLO(args.model)

    print("Model loaded successfully.")

    # ---------------------------------------------------------
    # UDP socket
    # ---------------------------------------------------------

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    # ---------------------------------------------------------
    # Open video
    # ---------------------------------------------------------

    cap = cv2.VideoCapture(args.video)

    if not cap.isOpened():
        print("ERROR: Cannot open video.")
        sock.close()
        return

    print("----------------------------------------")
    print(" YOLO OBJECT / ACCIDENT DETECTION")
    print("----------------------------------------")
    print("Model    :", args.model)
    print("Video    :", args.video)
    print("Receiver :", args.receiver)
    print("Port     :", args.port)
    print("----------------------------------------")

    # ---------------------------------------------------------
    # Accident class names
    #
    # CHANGE THESE according to your trained model.
    # Example:
    # ACCIDENT_CLASSES = ["accident", "crash"]
    # ---------------------------------------------------------

    ACCIDENT_CLASSES = [
        "accident",
        "crash"
    ]

    # ---------------------------------------------------------
    # Process video
    # ---------------------------------------------------------

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Video finished.")
            break

        # Run YOLO detection
        results = model(frame)

        detected_objects = []

        accident_detected = False

        # -----------------------------------------------------
        # Process detections
        # -----------------------------------------------------

        for box in results[0].boxes:

            class_id = int(box.cls[0])

            confidence = float(box.conf[0])

            class_name = model.names[class_id]

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            # Store detection
            detected_objects.append({
                "object": class_name,
                "confidence": round(
                    confidence,
                    2
                ),
                "bbox": [
                    x1,
                    y1,
                    x2,
                    y2
                ]
            })

            # -------------------------------------------------
            # Accident detection
            # -------------------------------------------------

            if class_name.lower() in [
                name.lower()
                for name in ACCIDENT_CLASSES
            ]:

                accident_detected = True

        # -----------------------------------------------------
        # Create V2X message
        # -----------------------------------------------------

        packet = {

            "device": "Vision Unit",

            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "accident_detected":
                accident_detected,

            "objects":
                detected_objects
        }

        # -----------------------------------------------------
        # Send information through UDP
        # -----------------------------------------------------

        message = json.dumps(packet)

        sock.sendto(
            message.encode(),
            (
                args.receiver,
                args.port
            )
        )

        # -----------------------------------------------------
        # Display detection result
        # -----------------------------------------------------

        annotated_frame = results[0].plot()

        # Display accident status
        if accident_detected:

            cv2.putText(
                annotated_frame,
                "ACCIDENT DETECTED",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 0, 255),
                3
            )

        else:

            cv2.putText(
                annotated_frame,
                "NORMAL",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3
            )

        cv2.imshow(
            "YOLO Accident Detection",
            annotated_frame
        )

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------

    cap.release()

    sock.close()

    cv2.destroyAllWindows()

    print("Detection stopped.")


if __name__ == "__main__":
    main()
