from unittest import TestCase
from rectpack.geometry import Rectangle, Point
import rectpack.maxrects as maxrects


class TestMaxRects(TestCase):

    def test_init(self):
        # Test initial maximal rectangle
        m = maxrects.MaxRects(20, 50)
        self.assertEqual(m._max_rects[0], Rectangle(0, 0, 20, 50))
        self.assertEqual(m.width, 20)
        self.assertEqual(m.height, 50)

    def test_reset(self):
        # Test _max_rects and rectangles is initialized
        m = maxrects.MaxRects(100, 200)
        self.assertTrue(m.add_rect(30, 30))
        self.assertTrue(m.add_rect(50, 50))
        self.assertEqual(len(m), 2)

        m.reset()
        self.assertEqual(len(m), 0)
        self.assertEqual(len(m._max_rects), 1)
        self.assertEqual(len(m.rectangles), 0)
        self.assertEqual(m._max_rects[0], Rectangle(0, 0, 100, 200))

    def test_add_rect(self):
        # Basic packing test.
        m = maxrects.MaxRects(200, 100)
        self.assertEqual(m.add_rect(50, 30), Rectangle(0, 0, 50, 30))
        self.assertEqual(len(m._max_rects), 2)
        self.assertEqual(m.add_rect(70, 200), Rectangle(0, 30, 200, 70))
        self.assertEqual(len(m._max_rects), 1)
        self.assertEqual(m.add_rect(20, 20), Rectangle(50, 0, 20, 20))
        self.assertEqual(len(m._max_rects), 2)
        self.assertEqual(m.add_rect(50, 50), None)
        self.assertEqual(m.add_rect(30, 100), Rectangle(70, 0, 100, 30))
        
        #Test with rotation disabled
        m = maxrects.MaxRects(200, 50, rot=False)
        self.assertEqual(m.add_rect(40, 80), None)
        
        m = maxrects.MaxRects(200, 50, rot=True)
        self.assertEqual(m.add_rect(40, 80), Rectangle(0, 0, 80, 40))

    def test_remove_duplicates(self):
        # Test duplicated collisions removed
        m = maxrects.MaxRects(100, 100)
        rect1 = Rectangle(0, 0, 60, 40)
        rect2 = Rectangle(30, 20, 60, 40)
        rect3 = Rectangle(35, 25, 10, 10)
        rect4 = Rectangle(90, 90, 10, 10)
        m._max_rects = [rect1, rect2, rect3, rect4]

        m._remove_duplicates()
        self.assertTrue(rect1 in m._max_rects)
        self.assertTrue(rect2 in m._max_rects)
        self.assertTrue(rect4 in m._max_rects)
        self.assertEqual(len(m._max_rects), 3)

        # Test with only one max_rect
        m = maxrects.MaxRects(100, 100)
        m._remove_duplicates()
        self.assertEqual(len(m._max_rects), 1)
        
    def test_iter(self):
        m = maxrects.MaxRects(100, 100)
        self.assertTrue(m.add_rect(10, 15))
        self.assertTrue(m.add_rect(40, 40))

        rectangles = []
        for r in m:
            rectangles.append(r)

        self.assertTrue(Rectangle(0, 0, 10, 15) in rectangles)
        self.assertTrue(Rectangle(10, 0, 40, 40) in rectangles)
        self.assertEqual(len(rectangles), 2)

    def test_fitness(self):
        mr = maxrects.MaxRects(100, 200, rot=True)
        m  = maxrects.MaxRects(100, 200, rot=False)
        self.assertEqual(m.fitness(200, 100), None)
        self.assertEqual(mr.fitness(200, 100), 0)
        self.assertEqual(m.fitness(100, 100), 0)

    def test_split(self):
        m = maxrects.MaxRects(100, 100)
        m.add_rect(20, 20)
        self.assertTrue(Rectangle(20, 0, 80, 100) in m._max_rects)
        self.assertTrue(Rectangle(0, 20, 100, 80) in m._max_rects)
        self.assertEqual(len(m._max_rects), 2)

        m._split(Rectangle(20, 20, 20, 20))
        self.assertEqual(len(m._max_rects), 6)
        m._remove_duplicates()
        self.assertEqual(len(m._max_rects), 4)

    def test_generate_splits(self):
        m = maxrects.MaxRects(40, 40)
        mr = Rectangle(20, 20, 40, 40)

        # The same
        rects = m._generate_splits(mr, Rectangle(20, 20, 40, 40))
        self.assertFalse(rects)

        # Contained
        rects = m._generate_splits(mr, Rectangle(0, 0, 80, 80))
        self.assertFalse(rects)

        # Center
        rects = m._generate_splits(mr, Rectangle(30, 30, 10, 10))
        self.assertTrue(Rectangle(20, 20, 10, 40) in rects) # Left
        self.assertTrue(Rectangle(20, 20, 40, 10) in rects) # Bottom
        self.assertTrue(Rectangle(40, 20, 20, 40) in rects) # Right
        self.assertTrue(Rectangle(20, 40, 40, 20) in rects) # Top
        self.assertEqual(len(rects), 4)

        # Top - Center
        rects = m._generate_splits(mr, Rectangle(30, 30, 10, 30))
        self.assertTrue(Rectangle(20, 20, 40, 10) in rects) # Bottom
        self.assertTrue(Rectangle(20, 20, 10, 40) in rects) # Left
        self.assertTrue(Rectangle(40, 20, 20, 40) in rects) # Right
        self.assertEqual(len(rects), 3)
 
        rects = m._generate_splits(mr, Rectangle(30, 30, 10, 100))
        self.assertTrue(Rectangle(20, 20, 40, 10) in rects) # Bottom
        self.assertTrue(Rectangle(20, 20, 10, 40) in rects) # Left
        self.assertTrue(Rectangle(40, 20, 20, 40) in rects) # Right
        self.assertEqual(len(rects), 3)

        # Bottom - Center
        rects = m._generate_splits(mr, Rectangle(30, 20, 10, 10))
        self.assertTrue(Rectangle(20, 30, 40, 30) in rects) # Top
        self.assertTrue(Rectangle(20, 20, 10, 40) in rects) # Left
        self.assertTrue(Rectangle(40, 20, 20, 40) in rects) # Right
        self.assertEqual(len(rects), 3)
        
        rects = m._generate_splits(mr, Rectangle(30, 0, 10, 30))
        self.assertTrue(Rectangle(20, 30, 40, 30) in rects) # Top
        self.assertTrue(Rectangle(20, 20, 10, 40) in rects) # Left
        self.assertTrue(Rectangle(40, 20, 20, 40) in rects) # Right
        self.assertEqual(len(rects), 3)

        # Left - Center
        rects = m._generate_splits(mr, Rectangle(20, 30, 20, 10))
        self.assertTrue(Rectangle(20, 40, 40, 20) in rects) # Top
        self.assertTrue(Rectangle(20, 20, 40, 10) in rects) # Bottom
        self.assertTrue(Rectangle(40, 20, 20, 40) in rects) # Right
        self.assertEqual(len(rects), 3)
        
        rects = m._generate_splits(mr, Rectangle(0, 30, 40, 10))
        self.assertTrue(Rectangle(20, 40, 40, 20) in rects) # Top
        self.assertTrue(Rectangle(20, 20, 40, 10) in rects) # Bottom
        self.assertTrue(Rectangle(40, 20, 20, 40) in rects) # Right
        self.assertEqual(len(rects), 3)

        # Right - Center
        rects = m._generate_splits(mr, Rectangle(40, 30, 20, 20))
        self.assertTrue(Rectangle(20, 50, 40, 10) in rects) # Top
        self.assertTrue(Rectangle(20, 20, 40, 10) in rects) # Bottom
        self.assertTrue(Rectangle(20, 20, 20, 40) in rects) # Left
        self.assertEqual(len(rects), 3)

        rects = m._generate_splits(mr, Rectangle(40, 30, 90, 20))
        self.assertTrue(Rectangle(20, 50, 40, 10) in rects) # Top
        self.assertTrue(Rectangle(20, 20, 40, 10) in rects) # Bottom
        self.assertTrue(Rectangle(20, 20, 20, 40) in rects) # Left
        self.assertEqual(len(rects), 3)

        # Top - Right
        rects = m._generate_splits(mr, Rectangle(40, 40, 20, 20))
        self.assertTrue(Rectangle(20, 20, 20, 40) in rects) # Left
        self.assertTrue(Rectangle(20, 20, 40, 20) in rects) # Bottom
        self.assertEqual(len(rects), 2)
        
        rects = m._generate_splits(mr, Rectangle(40, 40, 30, 30))
        self.assertTrue(Rectangle(20, 20, 20, 40) in rects) # Left
        self.assertTrue(Rectangle(20, 20, 40, 20) in rects) # Bottom
        self.assertEqual(len(rects), 2)
        
        # Bottom - Left 
        rects = m._generate_splits(mr, Rectangle(20, 20, 20, 20))
        self.assertTrue(Rectangle(20, 40, 40, 20) in rects) # Top
        self.assertTrue(Rectangle(40, 20, 20, 40) in rects) # Right
        self.assertEqual(len(rects), 2)
        
        rects = m._generate_splits(mr, Rectangle(10, 10, 30, 30))
        self.assertTrue(Rectangle(20, 40, 40, 20) in rects) # Top
        self.assertTrue(Rectangle(40, 20, 20, 40) in rects) # Right
        self.assertEqual(len(rects), 2)

        # Top - Full
        rects = m._generate_splits(mr, Rectangle(20, 40, 40, 20))
        self.assertTrue(Rectangle(20, 20, 40, 20) in rects)
        self.assertEqual(len(rects), 1)
        
        rects = m._generate_splits(mr, Rectangle(10, 40, 60, 60))
        self.assertTrue(Rectangle(20, 20, 40, 20) in rects)
        self.assertEqual(len(rects), 1)

        # Bottom - Full
        rects = m._generate_splits(mr, Rectangle(20, 20, 40, 20))
        self.assertTrue(Rectangle(20, 40, 40, 20) in rects)
        self.assertEqual(len(rects), 1)

        rects = m._generate_splits(mr, Rectangle(10, 10, 50, 30))
        self.assertTrue(Rectangle(20, 40, 40, 20) in rects)
        self.assertEqual(len(rects), 1)
        
        # Right - Full
        rects = m._generate_splits(mr, Rectangle(40, 20, 20, 40))
        self.assertTrue(Rectangle(20, 20, 20, 40) in rects)
        self.assertEqual(len(rects), 1)

        rects = m._generate_splits(mr, Rectangle(40, 10, 30, 60))
        self.assertTrue(Rectangle(20, 20, 20, 40) in rects)
        self.assertEqual(len(rects), 1)
        
        # Left - Full
        rects = m._generate_splits(mr, Rectangle(20, 20, 20, 40))
        self.assertTrue(Rectangle(40, 20, 20, 40) in rects)
        self.assertEqual(len(rects), 1)

        rects = m._generate_splits(mr, Rectangle(10, 10, 30, 60))
        self.assertTrue(Rectangle(40, 20, 20, 40) in rects)
        self.assertEqual(len(rects), 1)

    def test_getitem(self):
        m = maxrects.MaxRectsBl(100, 100, rot=False)
        m.add_rect(40, 40)
        m.add_rect(20, 20)
        m.add_rect(60, 40) 
        self.assertEqual(m[0], Rectangle(0, 0, 40, 40))
        self.assertEqual(m[1], Rectangle(40, 0, 20, 20))
        self.assertEqual(m[2], Rectangle(40, 20, 60, 40)) 

        self.assertEqual(m[-1], Rectangle(40, 20, 60, 40))
        self.assertEqual(m[1:],
                [Rectangle(40, 0, 20, 20), Rectangle(40, 20, 60, 40)])



class TestMaxRectBL(TestCase):

    def test_select_position(self):
        m = maxrects.MaxRectsBl(100, 100, rot=False)
        self.assertEqual(m.add_rect(40, 40), Rectangle(0, 0, 40, 40))
        self.assertFalse(m.add_rect(100, 100))

        self.assertEqual(m.add_rect(20, 20), Rectangle(40, 0, 20, 20))
        self.assertEqual(m.add_rect(60, 40), Rectangle(40, 20, 60, 40)) 


class TestMaxRectBAF(TestCase):

    def test_rect_fitness(self):
        m = maxrects.MaxRectsBaf(100, 100, rot=False)
        self.assertEqual(m.add_rect(60, 10), Rectangle(0, 0, 60, 10))

        self.assertTrue(m.fitness(40, 40) < m.fitness(50, 50))
        self.assertTrue(m.fitness(40, 40) < m.fitness(35, 35))
        self.assertEqual(m.add_rect(40, 40), Rectangle(60, 0, 40, 40))

class TestMaxRectBLSF(TestCase):
    
    def test_rect_fitnesss(self):
        m = maxrects.MaxRectsBlsf(100, 100, rot=False)
        self.assertEqual(m.add_rect(60, 10), Rectangle(0, 0, 60, 10))

        self.assertTrue(m.fitness(30, 90) < m.fitness(40, 89))
        self.assertTrue(m.fitness(99, 10) < m.fitness(99, 5))


class TestMaxRectBSSF(TestCase):
    
    def test_rect_fitness(self):
        m = maxrects.MaxRectsBssf(100, 100, rot=False)
        self.assertEqual(m.add_rect(60, 10), Rectangle(0, 0, 60, 10))

        self.assertTrue(m.fitness(30, 91) > m.fitness(30, 92))
        self.assertTrue(m.fitness(38, 91) < m.fitness(30, 92))
        self.assertTrue(m.fitness(38, 91) > m.fitness(40, 92))
