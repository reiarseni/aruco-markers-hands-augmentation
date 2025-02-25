# Aruco Markers Hands Augmentation

**A Python-based augmented reality project that combines real-time hand tracking using MediaPipe with ArUco marker detection to overlay dynamic images on real-world markers.**

## Description

This project demonstrates an augmented reality application built in Python. It integrates hand detection using MediaPipe with ArUco marker tracking to superimpose pre-defined augmented images over detected markers. The application features an interactive gesture-based interface to manipulate on-screen elements, a robust caching system to stabilize marker detection during temporary occlusions, and a modular code structure for clarity and maintainability.

## Features

- **ArUco Marker Detection:** Overlays augmented images on detected ArUco markers.
- **Hand Tracking:** Utilizes MediaPipe to detect and track hands, enabling gesture-based interactions.
- **Gesture-Based Interactions:** Allows users to move and pin on-screen elements using hand gestures.
- **Modular Architecture:** The project is organized into multiple modules for enhanced clarity and ease of extension.
- **Robust Caching System:** Maintains marker detection stability when markers are temporarily lost.

## Project Structure

- **main.py:** Main application file that integrates all modules and runs the AR experience.
- **augment_markers.py:** Logic for ArUco marker detection and image augmentation.
- **hand_detector.py:** Module for hand detection using MediaPipe.
- **marker_cache.py:** Caching system for maintaining detected marker data.
- **draggable_rectangle.py:** Implementation of draggable rectangles on the screen.
- **constants.py:** Configuration parameters for the project.


## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/reiarseni/aruco-markers-hands-augmentation.git
   cd aruco-markers-hands-augmentation
   ```

2. **Install the dependencies:**

   Ensure you have Python 3.6 or higher installed, then run:

   ```bash
   pip install opencv-python mediapipe numpy
   ```

3. **Augmented Marker Resources:**

   Place the marker images in the `augmented_markers` folder. Each image should be named with its corresponding marker ID.

## Usage

To start the application, run:

```bash
python main.py
```

- **Interactions:**  
  - Use hand gestures to control the cursor and interact with the on-screen elements.
  - Press the `q` key to exit the application.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is distributed under the **MIT License**. Please refer to the `LICENSE` file for more details.
