"""
Módulo para manejar el sistema de caché de marcadores ArUco.
"""

from typing import Optional, Tuple, List, Any
from constants import CACHE_MAX_LOST_FRAMES


class MarkerCache:
    """
    Clase para gestionar el caché de marcadores detectados.
    """

    def __init__(self, max_lost_frames: int = CACHE_MAX_LOST_FRAMES) -> None:
        self.cached_markers: Optional[Tuple[List[Any], List[Any]]] = None
        self.lost_frames_count: int = 0
        self.max_lost_frames: int = max_lost_frames
        self.pinned_markers: List[Tuple[List[Any], List[Any]]] = []
        self.pinned_marker_ids: List[int] = []

    def update_cache(self, new_markers: Tuple[List[Any], List[Any]]) -> Tuple[List[Any], List[Any]]:
        """
        Actualiza el caché con los nuevos marcadores detectados.

        Args:
            new_markers (Tuple[List[Any], List[Any]]): Tuple que contiene las bounding boxes y los IDs.

        Returns:
            Tuple[List[Any], List[Any]]: Marcadores actuales (nuevos o en caché).
        """
        bboxes, ids = new_markers

        if bboxes:
            self.lost_frames_count = 0
            self.cached_markers = new_markers
        else:
            self.lost_frames_count += 1
            if self.lost_frames_count >= self.max_lost_frames:
                self.cached_markers = None

            if self.cached_markers is not None:
                new_markers = self.cached_markers

        return new_markers

    def pin_marker(self, current_markers: Tuple[List[Any], List[Any]]) -> None:
        """
        Fija (pinea) el marcador detectado en el caché si no se ha fijado antes.

        Args:
            current_markers (Tuple[List[Any], List[Any]]): Marcadores actuales.
        """
        bboxes, ids = current_markers
        if ids is not None:
            for bbox, marker_id in zip(bboxes, ids):
                marker_id_int = int(marker_id)
                if marker_id_int not in self.pinned_marker_ids:
                    self.pinned_markers.append(current_markers)
                    print(marker_id_int)
                    self.pinned_marker_ids.append(marker_id_int)

    def clear_pinned_markers(self) -> None:
        """
        Limpia los marcadores fijados.
        """
        self.pinned_markers = []
        self.pinned_marker_ids = []
