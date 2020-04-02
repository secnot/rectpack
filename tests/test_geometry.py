from unittest import TestCase
from rectpack.geometry import Point, Segment, VSegment, HSegment, Rectangle




class TestPoint(TestCase):

    def test_init(self):
        p = Point(1, 2)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)

    def test_equality(self):
        p1 = Point(3, 4)
        p2 = Point(3, 4)
        p3 = Point(4, 3)

        self.assertTrue(p1==p2)
        self.assertFalse(p1==p3)
        self.assertFalse(p2==p3)

    def test_distance(self):
        p1 = Point(1, 1)
        p2 = Point(2, 1)

        self.assertEqual(p1.distance(p2), 1)


class TestSegment(TestCase):
    
    def test_init(self):
        s = Segment(Point(0,0), Point(3, 3))
        self.assertEqual(s.start, Point(0, 0))
        self.assertEqual(s.end, Point(3, 3))

        with self.assertRaises(AssertionError):
            Segment(Point(1, 1), 2)
        
        with self.assertRaises(AssertionError):
            Segment(2, Point(1, 1))

    def test_length(self):
        s = Segment(Point(0, 0), Point(0, 10))
        self.assertEqual(s.length, 10)

        s = Segment(Point(0, 0), Point(0, 3))
        self.assertEqual(s.length, 3)

    def test_maxmin(self):
        s = Segment(Point(1, 1), Point(5, 3))
        self.assertEqual(s.top, 3)
        self.assertEqual(s.bottom, 1)
        self.assertEqual(s.right, 5)
        self.assertEqual(s.left, 1)

    def test_eq(self):
        s1 = Segment(Point(0,0), Point(0, 10))
        s2 = Segment(Point(1, 1), Point(1, 11))
        s3 = Segment(Point(0, 0), Point(0, 10))
        self.assertEqual(s1, s3)
        self.assertNotEqual(s1, s2)

class TestHSegment(TestCase):

    def test_init(self):
        s = HSegment(Point(1, 1), 10)
        self.assertEqual(s.start, Point(1, 1))
        self.assertEqual(s.end, Point(11, 1))

        with self.assertRaises(AssertionError):
            HSegment(Point(1, 1), Point(1, 3))

        with self.assertRaises(AssertionError):
            HSegment(1, Point(1, 1))

    def test_length(self):
        s = HSegment(Point(10, 10), 10)
        self.assertEqual(s.length, 10)


class TestVSegment(TestCase):
    
    def test_init(self):
        s = VSegment(Point(1, 1), 10)
        self.assertEqual(s.start, Point(1, 1))
        self.assertEqual(s.end, Point(1, 11))

        with self.assertRaises(AssertionError):
            VSegment(Point(1, 1), Point(1, 3))

        with self.assertRaises(AssertionError):
            VSegment(1, Point(1, 1))

    def test_length(self):
        s = VSegment(Point(1, 1), 10)
        self.assertEqual(s.length, 10)


class TestRectangle(TestCase):

    def test_initialization(self):
        r = Rectangle(1, 2, 3, 4)
        self.assertEqual(r.left, 1)
        self.assertEqual(r.bottom, 2)
        self.assertEqual(r.right, 4)
        self.assertEqual(r.top, 6)
        self.assertEqual(r.width, 3)
        self.assertEqual(r.height, 4)

        self.assertEqual(r.corner_top_l, Point(1, 6))
        self.assertEqual(r.corner_top_r, Point(4, 6))
        self.assertEqual(r.corner_bot_l, Point(1, 2))
        self.assertEqual(r.corner_bot_r, Point(4, 2))

    def test_bool(self):
        """Test rectangles evaluates a True"""
        r = Rectangle(1, 2, 3, 4)
        self.assertTrue(r)

    def test_move(self):
        r = Rectangle(1, 2, 2, 2)
        self.assertEqual(r.bottom, 2)
        self.assertEqual(r.left, 1)
        
        r.move(10, 12)
        self.assertEqual(r.bottom, 12)
        self.assertEqual(r.left, 10)
        self.assertEqual(r.top,14)
        self.assertEqual(r.right, 12)
        self.assertEqual(r.height, 2)
        self.assertEqual(r.width, 2)

        self.assertEqual(r.corner_top_l, Point(10, 14))
        self.assertEqual(r.corner_top_r, Point(12, 14))
        self.assertEqual(r.corner_bot_l, Point(10, 12))
        self.assertEqual(r.corner_bot_r, Point(12, 12))

    def test_area(self):
        r1 = Rectangle(0, 0, 1, 2)
        r2 = Rectangle(1, 1, 2, 3)
        r3 = Rectangle(1, 1, 5, 5)

        self.assertEqual(r1.area(), 2)
        self.assertEqual(r2.area(), 6)

    def test_equal(self):
        r1 = Rectangle(0, 0, 1, 2)
        r2 = Rectangle(0, 0, 1, 1)
        r3 = Rectangle(1, 1, 1, 2)
        self.assertNotEqual(r1, r3)
        self.assertNotEqual(r1, r2)
        self.assertNotEqual(r2, r3)

        r4 = Rectangle(0, 0, 1, 2)
        self.assertEqual(r1, r4)
        
        r5 = Rectangle(1, 1, 1, 2)
        self.assertEqual(r3, r5)

    def test_lt(self):
        r1 = Rectangle(0, 0, 2, 1)
        r2 = Rectangle(0, 0, 1, 2)
        r3 = Rectangle(0, 0, 1, 3)

        self.assertFalse(r1 < r2)
        self.assertTrue(r1 < r3)
        self.assertTrue(r2 < r3)

    def test_hash(self):
        """Test it is hashable"""
        r = Rectangle(1, 1, 1, 1)
        d = {r: 43}

        self.assertEqual(d[r], 43)

    def test_intersects(self):
      
        # No intersections
        r  = Rectangle(20, 20, 4, 4)
        r1 = Rectangle(30, 30, 1, 1)
        r2 = Rectangle(20, 40, 2, 2)
        r3 = Rectangle(10, 10, 2, 2)

        self.assertFalse(r.intersects(r1))
        self.assertFalse(r.intersects(r2))
        self.assertFalse(r.intersects(r3))

        # Full contained intersects
        r = Rectangle(20, 20, 4, 4)
        r1 = Rectangle(21, 21, 2, 2)
        r2 = Rectangle(18, 18, 8, 8)
        self.assertTrue(r.intersects(r1))
        self.assertTrue(r.intersects(r2))

        # Area intersects
        r = Rectangle(10, 10, 2, 2)
        r_top = Rectangle(10, 11, 2 , 2)
        r_bottom = Rectangle(10, 9, 2, 2)
        r_right = Rectangle(11, 10, 2, 2)
        r_left = Rectangle(9, 10, 2, 2)
        self.assertTrue(r.intersects(r_top))
        self.assertTrue(r.intersects(r_bottom))
        self.assertTrue(r.intersects(r_right))
        self.assertTrue(r.intersects(r_left))

        r = Rectangle(10, 10, 2, 2)
        r_top_left = Rectangle(9, 11, 2, 2)
        r_top_right = Rectangle(11, 11, 2, 2)
        r_bottom_left = Rectangle(9, 9, 2, 2)
        r_bottom_right = Rectangle(11, 9, 2, 2)
        self.assertTrue(r.intersects(r_top_left))
        self.assertTrue(r.intersects(r_top_right))
        self.assertTrue(r.intersects(r_bottom_left))
        self.assertTrue(r.intersects(r_bottom_right))
        
        # Edge intersects
        r = Rectangle(10, 10, 2, 2)
        r_top = Rectangle(10, 12, 2, 2)
        r_bottom = Rectangle(10, 8, 2, 2)
        r_right = Rectangle(12, 10, 2, 2)
        r_left = Rectangle(8, 10, 2, 2)

        self.assertFalse(r.intersects(r_top))
        self.assertFalse(r.intersects(r_bottom))
        self.assertFalse(r.intersects(r_left))
        self.assertFalse(r.intersects(r_right))

        self.assertTrue(r.intersects(r_top, edges=True))
        self.assertTrue(r.intersects(r_bottom, edges=True))
        self.assertTrue(r.intersects(r_left, edges=True))
        self.assertTrue(r.intersects(r_right, edges=True))

        # Partial Edge intersects   
        r = Rectangle(10, 10, 2, 2)
        r_top = Rectangle(10, 12, 3, 2)
        r_bottom = Rectangle(10, 8, 1, 2)
        r_right = Rectangle(12, 10, 2, 1)
        r_left = Rectangle(8, 10, 2, 3)

        self.assertFalse(r.intersects(r_top))
        self.assertFalse(r.intersects(r_bottom))
        self.assertFalse(r.intersects(r_left))
        self.assertFalse(r.intersects(r_right))

        self.assertTrue(r.intersects(r_top, edges=True))
        self.assertTrue(r.intersects(r_bottom, edges=True))
        self.assertTrue(r.intersects(r_left, edges=True))
        self.assertTrue(r.intersects(r_right, edges=True))

        # Corner intersects
        r = Rectangle(10, 10, 2, 2)
        r_top_left = Rectangle(8, 12, 2, 2)
        r_top_right = Rectangle(12, 12, 2, 2)
        r_bottom_left = Rectangle(8, 8, 2, 2)
        r_bottom_right = Rectangle(12, 8, 2, 2)
        self.assertFalse(r.intersects(r_top_left))
        self.assertFalse(r.intersects(r_top_right))
        self.assertFalse(r.intersects(r_bottom_left))
        self.assertFalse(r.intersects(r_bottom_right))

        self.assertTrue(r.intersects(r_top_left, edges=True))
        self.assertTrue(r.intersects(r_top_right, edges=True))
        self.assertTrue(r.intersects(r_bottom_left, edges=True))
        self.assertTrue(r.intersects(r_bottom_right, edges=True))


    def test_intersection(self):
        
        # No intersection
        r  = Rectangle(20, 20, 4, 4)
        r1 = Rectangle(30, 30, 1, 1)
        r2 = Rectangle(20, 40, 2, 2)
        r3 = Rectangle(10, 10, 2, 2)

        self.assertFalse(r.intersection(r1))
        self.assertFalse(r.intersection(r2))
        self.assertFalse(r.intersection(r3))

        # Full contained intersection
        r = Rectangle(20, 20, 4, 4)
        r1 = Rectangle(21, 21, 2, 2)
        self.assertEqual(r1, r.intersection(r1))

        # Area intersection
        r = Rectangle(10, 10, 2, 2)
        r_top = Rectangle(10, 11, 2 , 2)
        r_bottom = Rectangle(10, 9, 2, 2)
        r_right = Rectangle(11, 10, 2, 2)
        r_left = Rectangle(9, 10, 2, 2)
        self.assertEqual(r.intersection(r_top), Rectangle(10, 11, 2, 1))
        self.assertEqual(r.intersection(r_bottom), Rectangle(10, 10, 2, 1))
        self.assertEqual(r.intersection(r_right), Rectangle(11, 10, 1, 2))
        self.assertEqual(r.intersection(r_left), Rectangle(10, 10, 1, 2))

        r = Rectangle(10, 10, 2, 4)
        r_top_left = Rectangle(9, 12, 2, 4)
        r_top_right = Rectangle(11, 12, 2, 4)
        r_bottom_left = Rectangle(9, 9, 2, 4)
        r_bottom_right = Rectangle(11, 9, 2, 4)
        self.assertEqual(r.intersection(r_top_left), Rectangle(10, 12, 1, 2))
        self.assertEqual(r.intersection(r_top_right), Rectangle(11, 12, 1, 2))
        self.assertEqual(r.intersection(r_bottom_left), Rectangle(10, 10, 1, 3))
        self.assertEqual(r.intersection(r_bottom_right), Rectangle(11, 10, 1, 3))
        
        # Edge intersection
        r = Rectangle(10, 10, 2, 2)
        r_top = Rectangle(10, 12, 3, 2)
        r_bottom = Rectangle(10, 8, 1, 2)
        r_left = Rectangle(8, 10, 2, 1)
        r_right = Rectangle(12, 10, 2, 1)
        self.assertEqual(r.intersection(r_top), None)
        self.assertEqual(r.intersection(r_bottom), None)
        self.assertEqual(r.intersection(r_left), None)
        self.assertEqual(r.intersection(r_right), None)

        self.assertEqual(r.intersection(r_top, edges=True), Rectangle(10, 12, 2, 0))
        self.assertEqual(r.intersection(r_bottom, edges=True), Rectangle(10, 10, 1, 0))
        self.assertEqual(r.intersection(r_left, edges=True), Rectangle(10, 10, 0, 1))
        self.assertEqual(r.intersection(r_right, edges=True), Rectangle(12, 10, 0,1))

        # Corners
        r = Rectangle(10, 10, 1, 1)
        r_top_r = Rectangle(11, 11, 1, 1)
        r_top_l = Rectangle(9, 11, 1, 1)
        r_bot_r = Rectangle(11, 9, 1, 1)
        r_bot_l = Rectangle(9, 9, 1, 1)

        self.assertEqual(r.intersection(r_top_r), None)
        self.assertEqual(r.intersection(r_top_l), None)
        self.assertEqual(r.intersection(r_bot_r), None)
        self.assertEqual(r.intersection(r_bot_l), None)

        self.assertEqual(r.intersection(r_top_r, edges=True), Rectangle(11, 11, 0, 0))
        self.assertEqual(r.intersection(r_top_l, edges=True), Rectangle(10, 11, 0, 0))
        self.assertEqual(r.intersection(r_bot_r, edges=True), Rectangle(11, 10, 0, 0))
        self.assertEqual(r.intersection(r_bot_l, edges=True), Rectangle(10, 10, 0, 0))

    def test_contains(self):
        
        # Outside
        r = Rectangle(1, 1, 3, 3)
        r1 = Rectangle(10, 10, 1, 2)
        self.assertFalse(r.contains(r1))

        # Part inside
        r = Rectangle(1, 1, 2, 2)
        r1 = Rectangle(2, 2, 4, 4)
        r2 = Rectangle(0, 1, 2, 3)
        r3 = Rectangle(0, 0, 4, 4)
        self.assertFalse(r.contains(r1))
        self.assertFalse(r.contains(r2))
        self.assertFalse(r.contains(r3))

        # Same size
        r = Rectangle(1, 1, 1, 1)
        r1 = Rectangle(1, 1, 1, 1)
        self.assertTrue(r.contains(r1))

        # Inside touching edges

        # Inside
        r = Rectangle(1, 1, 4, 4)
        r1 = Rectangle(2, 2, 1, 1)
        self.assertTrue(r.contains(r1))

    def test_join(self):
       
        # Top edge
        r = Rectangle(4, 4, 2, 2)
        r_top = Rectangle(4, 6, 2, 2)
        r_top_big = Rectangle(4, 6, 3, 2)

        self.assertFalse(r.join(r_top_big))
        self.assertTrue(r.join(r_top))
        self.assertEqual(r.corner_top_l, Point(4, 8))
        self.assertEqual(r.corner_top_r, Point(6, 8))
        self.assertEqual(r.corner_bot_l, Point(4, 4))
        self.assertEqual(r.corner_bot_r, Point(6, 4))

        # Bottom edge
        r = Rectangle(4, 4, 2, 2)
        r_bottom = Rectangle(4, 2, 2, 2)
        r_bottom_big = Rectangle(4, 2, 4, 2)

        self.assertFalse(r.join(r_bottom_big))
        self.assertTrue(r.join(r_bottom))
        self.assertEqual(r.corner_top_l, Point(4, 6))
        self.assertEqual(r.corner_top_r, Point(6, 6))
        self.assertEqual(r.corner_bot_l, Point(4, 2))
        self.assertEqual(r.corner_bot_r, Point(6, 2))

        # Right edge
        r = Rectangle(4, 4, 2, 2)
        r_right = Rectangle(6, 4, 3, 2)
        r_right_big = Rectangle(6, 4, 2, 4)

        self.assertFalse(r.join(r_right_big))
        self.assertTrue(r.join(r_right))
        self.assertEqual(r.corner_top_l, Point(4, 6))
        self.assertEqual(r.corner_top_r, Point(9, 6))
        self.assertEqual(r.corner_bot_l, Point(4, 4))
        self.assertEqual(r.corner_bot_r, Point(9, 4))

        # Left edge
        r = Rectangle(4, 4, 2, 2)
        r_left = Rectangle(2, 4, 2, 2)
        r_left_big = Rectangle(2, 4, 2, 4)

        self.assertFalse(r.join(r_left_big))
        self.assertTrue(r.join(r_left))
        self.assertEqual(r.corner_top_l, Point(2, 6))
        self.assertEqual(r.corner_top_r, Point(6, 6))
        self.assertEqual(r.corner_bot_l, Point(2, 4))
        self.assertEqual(r.corner_bot_r, Point(6, 4))

        # Contains
        r = Rectangle(4, 4, 3, 3)
        r_inside = Rectangle(4, 4, 1, 1)

        self.assertTrue(r.join(r_inside))
        self.assertEqual(r.corner_top_l, Point(4, 7))
        self.assertEqual(r.corner_top_r, Point(7, 7))
        self.assertEqual(r.corner_bot_l, Point(4, 4))
        self.assertEqual(r.corner_bot_r, Point(7, 4))

        # Is contained  
        r = Rectangle(4, 4, 1, 1)
        r_inside = Rectangle(4, 4, 3, 3)

        self.assertTrue(r.join(r_inside))
        self.assertEqual(r.corner_top_l, Point(4, 7))
        self.assertEqual(r.corner_top_r, Point(7, 7))
        self.assertEqual(r.corner_bot_l, Point(4, 4))
        self.assertEqual(r.corner_bot_r, Point(7, 4))

        # The same
        r = Rectangle(2, 2, 2, 2)
        r_same = Rectangle(2, 2, 2, 2)

        self.assertTrue(r.join(r_same))

    def test_iter(self):
        r = Rectangle(1, 1, 1, 2)
        corners = [Point(1, 1), Point(2, 1), Point(2, 3), Point(1,3)]

        for c in r:
            self.assertTrue(c in corners)
