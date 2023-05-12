"""Test case for the BoundingBox class

See https://code.visualstudio.com/docs/python/testing for how to set up 
testing in VSCode"""

__author__ = "François d'Entremont"

import unittest

from pyproj import CRS

import bbox
 

class TestBoundingBox(unittest.TestCase):
    """Bounding box test case"""

    def test_contains_true(self):
        # Create a new BoundingBox
        box = bbox.BoundingBox('', 0, 0, 2, 2, None)
        # A coordinate with the values 1,1 should be inside
        self.assertTrue(box.contains(1, 1))

    def test_contains_false(self):
        # Create a new BoundingBox
        box = bbox.BoundingBox('', 0, 0, 2, 2, None)
        # A coordinate with the values 3,2 should be outside
        self.assertFalse(box.contains(3, 2))

    def test_contains_touch_min_true(self):
        # A point that is on the edge should be considered inside
        box = bbox.BoundingBox('', 0, 0, 2, 2, None)
        # A coordinate with the values 3,2 should be outside
        self.assertTrue(box.contains(0, 0))

    def test_contains_touch_max_true(self):
        # A point that is on the edge should be considered inside
        box = bbox.BoundingBox('', 0, 0, 2, 2, None)
        # A coordinate with the values 3,2 should be outside
        self.assertTrue(box.contains(2, 2))

    def test_transform_to(self):
        # Create pyproj CRS
        crs = CRS.from_epsg(2961)
        # Create a bounding box
        box = bbox.BoundingBox('BBOX-1', 329000.0, 4972000.0,
         330000.0, 4973000.0, crs)
        # CRS that we will transform to
        epsg4617 = CRS.from_epsg(4617)
        box.transform_to(epsg4617)
        # The CRS should now be epsg4617
        self.assertTrue(box._crs == epsg4617)
        # Test the coordinates
        self.assertEqual(44.880895860232485, box._min_axis_0)
        self.assertEqual(-65.16514569988556, box._min_axis_1)
        self.assertEqual(44.890130890718865, box._max_axis_0)
        self.assertEqual(-65.1528286442206, box._max_axis_1)
