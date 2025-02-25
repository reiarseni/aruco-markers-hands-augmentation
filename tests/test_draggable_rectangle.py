"""
Unit tests for the draggable_rectangle module.
"""

import unittest

from draggable_rectangle import DragRectangle


class TestDragRectangle(unittest.TestCase):
    def test_update_inside_rectangle(self) -> None:
        # Test that update method correctly updates the center position when cursor is inside the rectangle
        rect = DragRectangle(center_position=(50, 50), size=(100, 100), color=(255, 0, 0))
        cursor = (60, 60)
        rect.update(cursor)
        self.assertEqual(rect.center_position, cursor)

    def test_update_outside_rectangle(self) -> None:
        # Test that update method does not change center position when cursor is outside the rectangle
        rect = DragRectangle(center_position=(50, 50), size=(100, 100), color=(255, 0, 0))
        cursor = (200, 200)
        rect.update(cursor)
        self.assertEqual(rect.center_position, (50, 50))


if __name__ == '__main__':
    unittest.main()

