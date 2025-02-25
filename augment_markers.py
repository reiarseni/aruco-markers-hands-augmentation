"""
Módulo para manejar la detección y aumento de marcadores ArUco.
"""

import cv2
import cv2.aruco as aruco
import numpy as np
import os
from typing import Tuple, List, Dict, Any

from constants import ARUCO_DICT, ARUCO_MARKER_SIZE, ARUCO_TOTAL_MARKERS


def load_augmented_images(folder_path: str) -> Dict[int, np.ndarray]:
    """
    Carga las imágenes de aumento para cada marcador desde la carpeta especificada.

    Args:
        folder_path (str): Ruta de la carpeta que contiene las imágenes.

    Returns:
        Dict[int, np.ndarray]: Diccionario con claves como IDs de marcador y valores como las imágenes.
    """
    augmented_images: Dict[int, np.ndarray] = {}
    try:
        image_files: List[str] = os.listdir(folder_path)
    except Exception as e:
        raise FileNotFoundError(f"No se pudo acceder a la carpeta {folder_path}: {e}")

    for image_file in image_files:
        try:
            # Se asume que el nombre del archivo es el ID del marcador
            marker_id: int = int(os.path.splitext(image_file)[0])
            image_path: str = os.path.join(folder_path, image_file)
            augmented_image: np.ndarray = cv2.imread(image_path)
            if augmented_image is None:
                raise ValueError(f"La imagen {image_path} no se pudo cargar.")
            augmented_images[marker_id] = augmented_image
        except Exception as e:
            print(f"Error al cargar la imagen {image_file}: {e}")

    return augmented_images


def find_aruco_markers(
    image: np.ndarray,
    marker_size: int = ARUCO_MARKER_SIZE,
    total_markers: int = ARUCO_TOTAL_MARKERS,
    draw: bool = True
) -> Tuple[List[Any], List[Any]]:
    """
    Detecta los marcadores ArUco en la imagen.

    Args:
        image (np.ndarray): Imagen en la que buscar marcadores.
        marker_size (int): Tamaño del marcador.
        total_markers (int): Número total de marcadores en el diccionario.
        draw (bool): Flag para dibujar el contorno de los marcadores.

    Returns:
        Tuple[List[Any], List[Any]]: Lista de contornos (bboxes) y IDs de marcadores detectados.
    """
    try:
        gray_image: np.ndarray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        raise ValueError(f"Error al convertir la imagen a escala de grises: {e}")

    # Crear el diccionario de ArUco
    aruco_dictionary = aruco.getPredefinedDictionary(ARUCO_DICT)
    aruco_parameters = aruco.DetectorParameters()

    # Crear el detector de ArUco
    detector = aruco.ArucoDetector(aruco_dictionary, aruco_parameters)

    bboxs, ids, _ = detector.detectMarkers(gray_image)

    if draw and bboxs:
        aruco.drawDetectedMarkers(image, bboxs)

    return bboxs, ids


def augment_aruco(
    bbox: Any,
    marker_id: int,
    image: np.ndarray,
    augmented_image: np.ndarray,
    draw_id: bool = True
) -> np.ndarray:
    """
    Superpone la imagen aumentada sobre el marcador ArUco detectado.

    Args:
        bbox (Any): Coordenadas del marcador.
        marker_id (int): ID del marcador.
        image (np.ndarray): Imagen base donde se realizará el aumento.
        augmented_image (np.ndarray): Imagen de aumento.
        draw_id (bool): Flag para mostrar el ID del marcador en la imagen.

    Returns:
        np.ndarray: Imagen con la superposición realizada.
    """
    # Extraer las coordenadas de las esquinas del marcador
    top_left = (bbox[0][0][0], bbox[0][0][1])
    top_right = (bbox[0][1][0], bbox[0][1][1])
    bottom_right = (bbox[0][2][0], bbox[0][2][1])
    bottom_left = (bbox[0][3][0], bbox[0][3][1])

    try:
        h_aug, w_aug, _ = augmented_image.shape
    except Exception as e:
        raise ValueError(f"Error al obtener las dimensiones de la imagen aumentada: {e}")

    pts_dst = np.array([top_left, top_right, bottom_right, bottom_left])
    pts_src = np.float32([[0, 0], [w_aug, 0], [w_aug, h_aug], [0, h_aug]])

    matrix, _ = cv2.findHomography(pts_src, pts_dst)
    img_warp = cv2.warpPerspective(augmented_image, matrix, (image.shape[1], image.shape[0]))

    # Rellenar el marcador detectado con negro para evitar superposición
    cv2.fillConvexPoly(image, pts_dst.astype(int), (0, 0, 0))
    img_out = image + img_warp

    if draw_id:
        cv2.putText(
            img_out,
            str(int(marker_id)),
            (int(bbox[0][0][0]), int(bbox[0][0][1])),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (255, 0, 0),
            3
        )

    return img_out
