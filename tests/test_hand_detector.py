"""
Unit tests for the hand_detector module.
"""

import cv2
import unittest
import numpy as np

from hand_detector import HandDetector


class TestHandDetector(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = HandDetector(max_hands=1)

    def test_find_hands_no_hand(self) -> None:
        # Create a blank image and expect no hands detected
        blank_image = np.zeros((480, 640, 3), dtype=np.uint8)
        result = self.detector.find_hands(blank_image.copy())
        self.assertIsInstance(result, np.ndarray)

    def test_find_position_no_hand(self) -> None:
        blank_image = np.zeros((480, 640, 3), dtype=np.uint8)
        self.detector.find_hands(blank_image.copy())
        lm_list, bbox = self.detector.find_position(blank_image.copy(), draw=False)
        # Expect no landmarks and default bounding box values when no hand is detected
        self.assertEqual(lm_list, [])
        self.assertEqual(bbox, (0, 0, 0, 0))


if __name__ == '__main__':
    unittest.main()

