"""
Archivo de constantes de configuración para la aplicación.
"""

import cv2

# Ruta de la carpeta que contiene las imágenes de los marcadores aumentados
AUGMENTED_MARKERS_PATH: str = "augmented_markers"

# Parámetros para la detección de manos
ENABLE_HAND_DETECTION: bool = True

# Parámetro para mostrar o no los rectángulos en pantalla
SHOW_RECTANGLES: bool = True

# Parámetros de la cámara
CAMERA_WIDTH: int = 800
CAMERA_HEIGHT: int = 600
FRAME_REDUCTION: int = 100  # Reducción del frame para la detección
SMOOTHENING: int = 7  # Suavizado para el movimiento

# Parámetros de ArUco
ARUCO_MARKER_SIZE: int = 6
ARUCO_TOTAL_MARKERS: int = 250
ARUCO_DICT: int = cv2.aruco.DICT_4X4_50

# Parámetros para el sistema de caché de marcadores
CACHE_MAX_LOST_FRAMES: int = 18

# Umbral para considerar un clic (distancia entre dedos)
CLICK_DISTANCE_THRESHOLD: float = 60.0

# Parámetro para optimizar la cantidad de frames procesados, se procesa solo el N-esimo frame, se saltan frames
FRAME_INTERVAL: int = 2
