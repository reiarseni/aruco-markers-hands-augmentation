"""
Módulo para la detección de manos utilizando MediaPipe.
"""

import cv2
import mediapipe as mp
import math
from typing import Tuple, List, Any


class HandDetector:
    """
    Clase para la detección de manos.
    """

    def __init__(
        self,
        mode: bool = False,
        max_hands: int = 2,
        detection_confidence: float = 0.9,
        tracking_confidence: float = 0.9
    ) -> None:
        self.mode: bool = mode
        self.max_hands: int = max_hands
        self.detection_confidence: float = detection_confidence
        self.tracking_confidence: float = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids: List[int] = [4, 8, 12, 16, 20]
        self.landmark_list: List[List[int]] = []

    def find_hands(self, image: Any, draw: bool = True) -> Any:
        """
        Detecta las manos en la imagen y dibuja las conexiones.

        Args:
            image (Any): Imagen en la que detectar las manos.
            draw (bool): Flag para dibujar las conexiones.

        Returns:
            Any: Imagen con las manos detectadas (si se solicita el dibujo).
        """
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_image)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )

        return image

    def find_position(self, image: Any, hand_no: int = 0, draw: bool = True) -> Tuple[List[List[int]], Tuple[int, int, int, int]]:
        """
        Encuentra la posición de cada landmark de la mano.

        Args:
            image (Any): Imagen en la que se detectan las manos.
            hand_no (int): Número de mano a procesar.
            draw (bool): Flag para dibujar los puntos y el rectángulo delimitador.

        Returns:
            Tuple[List[List[int]], Tuple[int, int, int, int]]:
                - Lista de landmarks con su ID y coordenadas.
                - Coordenadas del rectángulo delimitador (xmin, ymin, xmax, ymax).
        """
        x_list: List[int] = []
        y_list: List[int] = []
        bounding_box: Tuple[int, int, int, int] = (0, 0, 0, 0)
        self.landmark_list = []

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for idx, lm in enumerate(my_hand.landmark):
                h, w, _ = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_list.append(cx)
                y_list.append(cy)
                self.landmark_list.append([idx, cx, cy])
                if draw:
                    cv2.circle(image, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(x_list), max(x_list)
            ymin, ymax = min(y_list), max(y_list)
            bounding_box = (xmin, ymin, xmax, ymax)

            if draw:
                cv2.rectangle(image, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)

        return self.landmark_list, bounding_box

    def fingers_up(self) -> List[int]:
        """
        Determina qué dedos están levantados.

        Returns:
            List[int]: Lista de 0s y 1s indicando si cada dedo está levantado.
        """
        fingers: List[int] = []

        if not self.landmark_list:
            return fingers

        # Pulgar
        if self.landmark_list[self.tip_ids[0]][1] > self.landmark_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Resto de los dedos
        for idx in range(1, 5):
            if self.landmark_list[self.tip_ids[idx]][2] < self.landmark_list[self.tip_ids[idx] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def find_distance(self, point1: int, point2: int, image: Any, draw: bool = True, radius: int = 15, thickness: int = 3) -> Tuple[float, Any, List[int]]:
        """
        Calcula la distancia entre dos landmarks.

        Args:
            point1 (int): Índice del primer landmark.
            point2 (int): Índice del segundo landmark.
            image (Any): Imagen para dibujar la distancia.
            draw (bool): Flag para dibujar la línea y círculos.
            radius (int): Radio de los círculos.
            thickness (int): Grosor de la línea.

        Returns:
            Tuple[float, Any, List[int]]:
                - Distancia entre los puntos.
                - Imagen con la representación gráfica.
                - Lista de coordenadas [x1, y1, x2, y2, cx, cy].
        """
        x1, y1 = self.landmark_list[point1][1], self.landmark_list[point1][2]
        x2, y2 = self.landmark_list[point2][1], self.landmark_list[point2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), thickness)
            cv2.circle(image, (x1, y1), radius, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), radius, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (cx, cy), radius, (0, 0, 255), cv2.FILLED)

        distance: float = math.hypot(x2 - x1, y2 - y1)

        return distance, image, [x1, y1, x2, y2, cx, cy]
