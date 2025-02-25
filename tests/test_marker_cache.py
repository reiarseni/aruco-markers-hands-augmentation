"""
Unit tests for the marker_cache module.
"""

import unittest

from marker_cache import MarkerCache


class TestMarkerCache(unittest.TestCase):
    def setUp(self) -> None:
        self.cache = MarkerCache(max_lost_frames=3)

    def test_update_cache_empty(self) -> None:
        # Test update_cache with empty markers
        empty_markers = ([], None)
        result = self.cache.update_cache(empty_markers)
        self.assertEqual(result, empty_markers)
        self.assertIsNone(self.cache.cached_markers)

    def test_update_cache_non_empty(self) -> None:
        # Test update_cache with non-empty markers
        dummy_bbox = [[[ [10, 10], [110, 10], [110, 110], [10, 110] ]]]
        dummy_ids = [1]
        non_empty_markers = (dummy_bbox, dummy_ids)
        result = self.cache.update_cache(non_empty_markers)
        self.assertEqual(result, non_empty_markers)
        self.assertEqual(self.cache.cached_markers, non_empty_markers)

    def test_pin_and_clear_markers(self) -> None:
        # Test pin_marker and clear_pinned_markers functions
        dummy_bbox = [[[ [10, 10], [110, 10], [110, 110], [10, 110] ]]]
        dummy_ids = [1]
        non_empty_markers = (dummy_bbox, dummy_ids)
        self.cache.cached_markers = non_empty_markers
        self.cache.pin_marker(non_empty_markers)
        self.assertIn(1, self.cache.pinned_marker_ids)
        self.cache.clear_pinned_markers()
        self.assertEqual(self.cache.pinned_markers, [])
        self.assertEqual(self.cache.pinned_marker_ids, [])


if __name__ == '__main__':
    unittest.main()

