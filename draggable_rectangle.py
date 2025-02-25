"""
Módulo para manejar los rectángulos desplazables en la pantalla.
"""

from typing import Tuple


class DragRectangle:
    """
    Clase que representa un rectángulo desplazable.
    """

    def __init__(self, center_position: Tuple[int, int], size: Tuple[int, int] = (100, 100),
                 color: Tuple[int, int, int] = (255, 0, 255)) -> None:
        self.center_position: Tuple[int, int] = center_position
        self.size: Tuple[int, int] = size
        self.color: Tuple[int, int, int] = color

    def update(self, cursor: Tuple[int, int]) -> None:
        """
        Actualiza la posición del rectángulo si el cursor se encuentra dentro del mismo.

        Args:
            cursor (Tuple[int, int]): Posición actual del cursor.
        """
        cx, cy = self.center_position
        width, height = self.size

        # Verificar si el cursor está dentro del rectángulo
        if cx - width // 2 < cursor[0] < cx + width // 2 and cy - height // 2 < cursor[1] < cy + height // 2:
            self.center_position = cursor
