# V2X Perception and Mapping System

A multi-modal Vehicle-to-Everything (V2X) testbed integrating vision-based perception, LiDAR-based obstacle detection, Wi-Fi 6 communication, and UWB-based real-time vehicle localization and mapping visualization.

---

## 📌 Overview

This project focuses on the development and demonstration of different technologies required for an indoor V2X environment.

The system combines:

- Camera-based object and accident detection using YOLO
- LiDAR-based obstacle and distance detection using RPLIDAR
- Wi-Fi 6-based wireless communication using UDP
- UWB-based real-time vehicle/tag localization
- 2D visualization of the localized vehicle/tag position

The individual modules were developed and tested as part of a V2X perception, communication, and localization testbed.

---

## 🎯 Project Objectives

The main objectives of this project are:

- Develop a vision-based perception system for detecting objects and accident-related events.
- Use LiDAR to detect nearby obstacles and obtain distance information.
- Demonstrate wireless communication between devices using a Wi-Fi 6 network.
- Transmit real-time video and data between devices.
- Implement UWB-based real-time indoor localization.
- Estimate the position of a mobile tag using multiple fixed UWB anchors.
- Visualize the vehicle/tag position in a 2D environment.
- Provide a foundation for integrating perception, localization, communication, and mapping in V2X applications.

---

# 🏗️ System Architecture

```text
                         V2X SYSTEM
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   PERCEPTION          LOCALIZATION        COMMUNICATION
        │                    │                    │
   ┌────┴────┐              UWB                Wi-Fi 6
   │         │               │                    │
 Camera     LiDAR            │              Video / Data
   │         │               │                    │
  YOLO    RPLIDAR            ▼                    │
   │         │        Vehicle / Tag Position      │
   │         │               │                    │
   └────┬────┘               ▼                    │
        │              2D Visualization           │
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
                    V2X Environment
👁️ 1. Vision-Based Perception

The vision module uses a camera/video input and YOLO-based object detection.

Object Detection

A YOLO-based object detection application was developed using Python and OpenCV.

The system:

Reads a video input.
Processes the video frame by frame.
Runs YOLO inference.
Detects objects.
Draws bounding boxes around detected objects.
Displays the annotated video.
Technologies
Python
OpenCV
Ultralytics YOLO
Source Code
perception/
└── vision/
    └── object_detection/
        └── yolo_object_detection.py
Accident Detection

A trained YOLO model was developed for the project's object/accident detection application.

The available implementation demonstrates YOLO inference and transmission of detected-object information to another device using UDP.

The transmitted information can include:

Detected object/class
Detection confidence
Bounding-box coordinates
Timestamp
Accident-related detection information
Trained Model
models/
└── vision/
    └── best.pt

The trained model and demonstration results are included separately from the basic object-detection source code.

📡 2. LiDAR-Based Perception

The LiDAR application uses an RPLIDAR sensor for nearby object and obstacle detection.

The demonstrated application was used to:

Scan the surrounding environment
Detect nearby objects/obstacles
Observe distance information
Provide perception information for the V2X testbed
Hardware
RPLIDAR
Results

Demonstration videos are provided in:

results/
└── lidar/

The original source code for this particular LiDAR implementation is not currently available, therefore this repository does not claim to contain the original LiDAR source code.

📶 3. Wi-Fi 6 Communication

Wi-Fi 6 was used as the wireless communication network between devices.

The communication experiments demonstrated transmission of real-time information between devices using UDP-based communication.

Demonstrated Applications
Live Video Streaming
Video Input
     ↓
Video Processing
     ↓
H.264 / RTP
     ↓
UDP
     ↓
Wi-Fi 6
     ↓
Receiver
     ↓
Live Video
Screen / Desktop Sharing

The communication setup was also used to demonstrate wireless sharing of live screen/desktop content between devices.

Data Transmission

The system can also be used to transmit raw or structured data between devices over the wireless network.

Example Structure
communication/
└── wifi6/
    └── video_streaming/
        ├── sender.py
        └── receiver.py

The reusable communication examples in this repository are reference/reconstructed implementations based on the demonstrated application. They are not claimed to be the original lost source code.

📍 4. UWB Localization and Mapping

The localization component provides the main positional information used for the project's 2D mapping visualization.

A UWB-based indoor localization system was developed using multiple fixed anchors and a mobile tag.

Localization Process
UWB Anchors
    │
    ▼
Distance Measurements
    │
    ▼
Distance Processing
    │
    ▼
Trilateration /
Multilateration
    │
    ▼
X,Y Position
    │
    ▼
2D Visualization

The system supports localization using multiple UWB anchors and calculates the position of the mobile tag.

Source Code
localization/
└── uwb/
    ├── config.py
    ├── parser.py
    ├── trilateration.py
    ├── plotter.py
    └── uwb_localization.py
Main Components
File	Function
config.py	Anchor configuration and localization parameters
parser.py	Processes UWB ranging information
trilateration.py	Calculates the tag position
plotter.py	Provides the real-time localization visualization
uwb_localization.py	Main program for running the localization system
🗺️ UWB-Based 2D Mapping Visualization

In this project, the term mapping refers to the 2D visualization of the UWB-localized vehicle/tag position.

The visualization shows the relationship between:

Fixed UWB anchors
Mobile tag
Measured distances
Estimated X/Y position
Localization status

Example concept:

        A2                         A4
        ●--------------------------●
        |                          |
        |            TAG           |
        |             ●            |
        |                          |
        ●--------------------------●
        A1                         A3

The UWB localization result provides the position information that can be used as a positional input for future V2X mapping and navigation applications.

🔄 Integrated V2X Concept

The individual modules can be viewed as complementary parts of a V2X system:

                 ┌───────────────────┐
                 │     VEHICLE       │
                 └─────────┬─────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
          Camera         LiDAR          UWB
             │             │             │
             ▼             ▼             ▼
           YOLO         Obstacles     Position
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                     V2X Processing
                           │
                           ▼
                      Wi-Fi 6 / UDP
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
              Vehicle A         Vehicle B
🧰 Hardware

The project involved the following types of hardware:

Raspberry Pi
NVIDIA Jetson platform
Qorvo UWB development boards
RPLIDAR
Camera
Wi-Fi 6 networking equipment
💻 Software and Technologies
Python
OpenCV
Ultralytics YOLO
NumPy
Matplotlib
UDP
Wi-Fi 6
UWB
RPLIDAR
Linux
Git / GitHub
📁 Project Structure
V2X-Perception-and-Mapping-System/
│
├── perception/
│   ├── vision/
│   │   └── object_detection/
│   │       └── yolo_object_detection.py
│   │
│   └── lidar/
│
├── localization/
│   └── uwb/
│       ├── config.py
│       ├── parser.py
│       ├── trilateration.py
│       ├── plotter.py
│       └── uwb_localization.py
│
├── communication/
│   └── wifi6/
│       └── video_streaming/
│           ├── sender.py
│           └── receiver.py
│
├── models/
│   └── vision/
│       └── best.pt
│
├── results/
│   ├── vision/
│   ├── lidar/
│   ├── wifi6/
│   └── uwb_mapping/
│
├── documentation/
│
├── README.md
├── requirements.txt
└── .gitignore
📊 Experimental Results

The repository contains demonstration material for the different modules.

Vision
YOLO object detection demonstrations
Accident/object detection demonstrations
Trained model
LiDAR
RPLIDAR obstacle detection demonstrations
Distance detection demonstrations
Wi-Fi 6
Live video transmission
Screen/desktop sharing
Wireless data communication demonstrations
UWB
Real-time anchor/tag visualization
Distance measurements
X/Y position estimation
2D localization visualization
⚠️ Current Scope and Limitations
The project consists of several independently developed and demonstrated V2X modules.
The original source code for the LiDAR application is not currently available.
Some Wi-Fi 6 communication examples in this repository are reconstructed reusable examples based on the demonstrated communication concept and are not claimed to be the original source code.
The available UWB implementation focuses on real-time indoor localization and visualization.
A comprehensive quantitative accuracy evaluation of the complete integrated V2X system is outside the current scope.
The modules are not presented as a fully production-ready automotive V2X system.
🚀 Future Improvements

Potential future development includes:

Integrating camera, LiDAR and UWB data into a unified perception system.
Sensor fusion between UWB and LiDAR.
Improved vehicle tracking.
Real-time environmental mapping.
Integration with ROS/ROS2.
Improved V2V/V2X message formats.
Low-latency video and data communication.
Edge-AI-based perception on Jetson hardware.
Quantitative localization accuracy evaluation.
Real-time multi-vehicle experiments.
Collision-warning and safety applications.
🎯 Applications

The developed technologies can support future applications such as:

Vehicle localization
Obstacle detection
Accident awareness
Vehicle-to-vehicle communication
Real-time video sharing
Emergency warning
Collision avoidance
Indoor vehicle tracking
Intelligent transportation systems
👨‍💻 Author

Abhilash Jyothi

Electronics and Communication Engineering

V2X Perception, Localization and Communication Project
