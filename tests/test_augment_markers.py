"""
Unit tests for the augment_markers module.
"""

import os
import cv2
import unittest
import numpy as np
import tempfile
import shutil

from augment_markers import load_augmented_images, find_aruco_markers, augment_aruco
import constants


class TestAugmentMarkers(unittest.TestCase):
    def setUp(self) -> None:
        # Create a temporary directory for augmented marker images
        self.test_dir = tempfile.mkdtemp()
        # Create a dummy image file for marker with id 1
        self.dummy_image_path = os.path.join(self.test_dir, "1.png")
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imwrite(self.dummy_image_path, dummy_image)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)

    def test_load_augmented_images(self) -> None:
        # Test that the dummy image is loaded correctly
        images = load_augmented_images(self.test_dir)
        self.assertIn(1, images)
        self.assertIsInstance(images[1], np.ndarray)

    def test_find_aruco_markers_no_marker(self) -> None:
        # Create a blank image that should not contain any markers
        blank_image = np.zeros((480, 640, 3), dtype=np.uint8)
        bboxes, ids = find_aruco_markers(blank_image, draw=False)
        # Expect no markers found
        self.assertEqual(bboxes, [])
        self.assertIsNone(ids)

    def test_augment_aruco_with_valid_input(self) -> None:
        # Create dummy inputs to test augment_aruco function
        dummy_bbox = [[[ [10, 10], [110, 10], [110, 110], [10, 110] ]]]
        dummy_marker_id = 1
        dummy_base_image = np.zeros((200, 200, 3), dtype=np.uint8)
        dummy_augmented_image = np.zeros((100, 100, 3), dtype=np.uint8)
        # Test that the function runs without error and returns an image
        result_image = augment_aruco(dummy_bbox, dummy_marker_id, dummy_base_image.copy(), dummy_augmented_image)
        self.assertIsInstance(result_image, np.ndarray)


if __name__ == '__main__':
    unittest.main()

