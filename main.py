"""
Aplicación principal de realidad aumentada utilizando detección de marcadores ArUco y manos.
"""

import cv2
import time
import numpy as np

from augment_markers import load_augmented_images, find_aruco_markers, augment_aruco
from hand_detector import HandDetector
from marker_cache import MarkerCache
from draggable_rectangle import DragRectangle
import constants


def main() -> None:
    """
    Función principal de la aplicación.
    """
    # Inicializar la captura de video
    try:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, constants.CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, constants.CAMERA_HEIGHT)
    except Exception as e:
        print(f"Error al iniciar la captura de video: {e}")
        return

    # Cargar las imágenes de aumento para los marcadores
    try:
        augmented_images = load_augmented_images(constants.AUGMENTED_MARKERS_PATH)
    except Exception as e:
        print(f"Error al cargar las imágenes aumentadas: {e}")
        return

    # Inicializar el detector de manos si está habilitado
    hand_detector = HandDetector(max_hands=2) if constants.ENABLE_HAND_DETECTION else None

    # Inicializar la caché de marcadores
    marker_cache = MarkerCache()

    # Inicializar los rectángulos desplazables
    drag_rectangles = [
        DragRectangle(center_position=(100, 100), size=(100, 100), color=(255, 0, 255)),
        DragRectangle(center_position=(300, 100), size=(100, 100), color=(255, 255, 0)),
        DragRectangle(center_position=(500, 100), size=(100, 100), color=(0, 255, 255))
    ]

    # Variables para el control del movimiento
    prev_time: float = 0.0
    prev_loc_x, prev_loc_y = 0, 0
    curr_loc_x, curr_loc_y = 0, 0

    # Variables para la detección de dedos
    frame_reduction = constants.FRAME_REDUCTION
    smoothening = constants.SMOOTHENING

    # Variable para el cursor
    cursor = (0, 0)

    # New variables for frame skipping
    frame_interval: int = 2  # Process only every 2nd frame
    frame_count: int = 0
    last_processed_frame = None

    while True:
        # Capturar frame de la cámara
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el frame de la cámara.")
            break

        # Check if we should process this frame or use the last processed frame
        if frame_count % frame_interval == 0:
            # Detección de manos si está habilitada
            if constants.ENABLE_HAND_DETECTION and hand_detector is not None:
                frame = hand_detector.find_hands(frame)
                landmark_list, _ = hand_detector.find_position(frame, draw=False)
                if landmark_list:
                    # Obtener la posición del índice y del dedo medio
                    x_index, y_index = landmark_list[8][1], landmark_list[8][2]
                    x_middle, y_middle = landmark_list[12][1], landmark_list[12][2]
                    fingers = hand_detector.fingers_up()

                    # Modo de movimiento: solo el índice levantado
                    if len(fingers) > 0 and fingers[1] == 1 and fingers[2] == 0:
                        # Convertir coordenadas
                        screen_x = np.interp(
                            x_index,
                            (frame_reduction, constants.CAMERA_WIDTH - frame_reduction),
                            (0, constants.CAMERA_WIDTH)
                        )
                        screen_y = np.interp(
                            y_index,
                            (frame_reduction, constants.CAMERA_HEIGHT - frame_reduction),
                            (0, constants.CAMERA_HEIGHT)
                        )
                        # Suavizar el movimiento
                        curr_loc_x = int(prev_loc_x + (screen_x - prev_loc_x) / smoothening)
                        curr_loc_y = int(prev_loc_y + (screen_y - prev_loc_y) / smoothening)
                        prev_loc_x, prev_loc_y = curr_loc_x, curr_loc_y
                        # Dibujar el cursor en la imagen
                        cv2.circle(frame, (x_index, y_index), 15, (255, 0, 255), cv2.FILLED)
                        cursor = (x_index, y_index)
                        # Actualizar la posición de los rectángulos desplazables
                        for rect in drag_rectangles:
                            rect.update(cursor)

                    # Modo de clic: índice y dedo medio levantados
                    if len(fingers) > 0 and fingers[1] == 1 and fingers[2] == 1:
                        distance, frame, line_info = hand_detector.find_distance(8, 12, frame)
                        if distance < constants.CLICK_DISTANCE_THRESHOLD:
                            cv2.circle(frame, (line_info[4], line_info[5]), 15, (0, 255, 0), cv2.FILLED)
                            # Fijar el marcador en la caché
                            if marker_cache.cached_markers is not None:
                                marker_cache.pin_marker(marker_cache.cached_markers)
                        else:
                            marker_cache.clear_pinned_markers()

            # Detección de marcadores ArUco
            aruco_bboxes, aruco_ids = find_aruco_markers(frame)
            current_markers = (aruco_bboxes, aruco_ids)
            current_markers = marker_cache.update_cache(current_markers)

            # Superponer la imagen aumentada en cada marcador detectado
            if current_markers[0]:
                for bbox, marker_id in zip(current_markers[0], current_markers[1]):
                    marker_id_int = int(marker_id)
                    if marker_id_int in augmented_images:
                        frame = augment_aruco(bbox, marker_id_int, frame, augmented_images[marker_id_int])

            # Mostrar los marcadores fijados (pinned)
            if marker_cache.pinned_markers:
                for pinned_markers in marker_cache.pinned_markers:
                    for bbox, marker_id in zip(pinned_markers[0], pinned_markers[1]):
                        marker_id_int = int(marker_id)
                        if marker_id_int in augmented_images:
                            frame = augment_aruco(bbox, marker_id_int, frame, augmented_images[marker_id_int])

            # Dibujar los rectángulos desplazables si está habilitado
            if constants.SHOW_RECTANGLES:
                overlay = np.zeros_like(frame, np.uint8)
                for rect in drag_rectangles:
                    cx, cy = rect.center_position
                    width, height = rect.size
                    top_left = (cx - width // 2, cy - height // 2)
                    bottom_right = (cx + width // 2, cy + height // 2)
                    cv2.rectangle(overlay, top_left, bottom_right, rect.color, cv2.FILLED)
                alpha = 0.5
                mask = overlay.astype(bool)
                frame[mask] = cv2.addWeighted(frame, alpha, overlay, 1 - alpha, 0)[mask]

            # Calcular y mostrar el FPS
            current_time = time.time()
            fps = 1 / (current_time - prev_time) if current_time - prev_time > 0 else 0
            prev_time = current_time
            cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

            # Store the processed frame
            last_processed_frame = frame.copy()
        else:
            # Use the last processed frame for display if available
            if last_processed_frame is not None:
                frame = last_processed_frame.copy()

        cv2.imshow("Augmented Reality", frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

