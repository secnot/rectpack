from unittest import TestCase

from rectpack.geometry import Rectangle
from rectpack.pack_algo import PackingAlgorithm


class TestPackingValidation(TestCase):

    def setUp(self):
        self.packing = PackingAlgorithm(10, 10)

    def test_empty_packing(self):
        self.packing.validate_packing()

    def test_single_rectangle(self):
        self.packing.rectangles = [Rectangle(0, 0, 2, 2)]
        self.packing.validate_packing()

    def test_two_overlapping_rectangles(self):
        self.packing.rectangles = [
            Rectangle(0, 0, 2, 2),
            Rectangle(1, 1, 2, 2),
        ]
        with self.assertRaisesRegex(Exception, "Rectangle collision detected"):
            self.packing.validate_packing()

    def test_collision_between_first_and_last_rectangles(self):
        self.packing.rectangles = [
            Rectangle(0, 0, 2, 2),
            Rectangle(5, 5, 2, 2),
            Rectangle(1, 1, 2, 2),
        ]
        with self.assertRaisesRegex(Exception, "Rectangle collision detected"):
            self.packing.validate_packing()

    def test_collision_between_last_two_rectangles(self):
        self.packing.rectangles = [
            Rectangle(0, 0, 2, 2),
            Rectangle(5, 5, 2, 2),
            Rectangle(6, 6, 2, 2),
        ]
        with self.assertRaisesRegex(Exception, "Rectangle collision detected"):
            self.packing.validate_packing()

    def test_non_overlapping_rectangles(self):
        self.packing.rectangles = [
            Rectangle(0, 0, 2, 2),
            Rectangle(4, 4, 2, 2),
            Rectangle(8, 8, 2, 2),
        ]
        self.packing.validate_packing()

    def test_rectangles_touching_edges_and_corners(self):
        self.packing.rectangles = [
            Rectangle(0, 0, 2, 2),
            Rectangle(2, 0, 2, 2),
            Rectangle(4, 2, 2, 2),
        ]
        self.packing.validate_packing()

    def test_rectangle_outside_surface(self):
        self.packing.rectangles = [Rectangle(9, 9, 2, 2)]
        with self.assertRaisesRegex(Exception, "Rectangle placed outside surface"):
            self.packing.validate_packing()
