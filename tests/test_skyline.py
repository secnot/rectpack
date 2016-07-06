from unittest import TestCase
from rectpack.geometry import Rectangle
import rectpack.skyline as skyline


class TestSkyline(TestCase):

    def test_init(self):
        s = skyline.SkylineBl(100, 100, rot=False)
        rect1 = s.add_rect(30, 30)
        rect2 = s.add_rect(100, 70)
        self.assertEqual(rect1, Rectangle(0, 0, 30, 30))
        self.assertEqual(rect2, Rectangle(0, 30, 100, 70))
  
    def test_rotation(self):
        # Test rotation is enabled by default
        s = skyline.SkylineBl(100, 10)
        rect1 = s.add_rect(10, 100)
        self.assertEqual(rect1, Rectangle(0, 0, 100, 10))

        # Test rotation can be disabled
        s = skyline.SkylineBl(100, 10, rot=False)
        rect1 = s.add_rect(10, 100)
        self.assertEqual(rect1, None)

    def test_waste_management(self):
        # Generate one wasted section
        s = skyline.SkylineBlWm(100, 100, rot=False)
        rect1 = s.add_rect(30, 30)
        rect2 = s.add_rect(100, 70)
        self.assertEqual(rect1, Rectangle(0, 0, 30, 30))
        self.assertEqual(rect2, Rectangle(0, 30, 100, 70))
        self.assertEqual(len(s), 2)
        
        # Add rectangle that only fits into wasted section
        self.assertEqual(s.add_rect(71, 30), None)
        self.assertEqual(s.add_rect(70, 31), None) 
        rect3 = s.add_rect(70, 30)
        self.assertEqual(rect3, Rectangle(30, 0, 70, 30))
        self.assertEqual(len(s), 3)
        
        rect4 = s.add_rect(70, 30)
        self.assertEqual(rect4, None)

        # Test the same without waste management
        s = skyline.SkylineBl(100, 100)
        rect1 = s.add_rect(30, 30)
        rect2 = s.add_rect(100, 70)
        self.assertEqual(rect1, Rectangle(0, 0, 30, 30))
        self.assertEqual(rect2, Rectangle(0, 30, 100, 70))
        
        self.assertEqual(s.add_rect(70, 30), None)
        self.assertEqual(len(s), 2)

        # Test waste supports rectangle rotation
        s  = skyline.SkylineBlWm(100, 100, rot=False)
        sr = skyline.SkylineBlWm(100, 100, rot=True)
        self.assertEqual(s.add_rect(30, 30), Rectangle(0, 0, 30, 30))
        self.assertEqual(s.add_rect(100, 70), Rectangle(0, 30, 100, 70))
        self.assertEqual(sr.add_rect(30, 30), Rectangle(0, 0, 30, 30))
        self.assertEqual(sr.add_rect(100, 70), Rectangle(0, 30, 100, 70))
        
        self.assertEqual(s.add_rect(30, 70), None)
        self.assertEqual(sr.add_rect(30, 70), Rectangle(30, 0, 70, 30))
        
        # Try with more than one wasted section
        s = skyline.SkylineBlWm(100, 100, rot=False)
        self.assertEqual(s.add_rect(40, 50), Rectangle(0, 0, 40, 50))
        self.assertEqual(s.add_rect(20, 30), Rectangle(40, 0, 20, 30))
        self.assertEqual(s.add_rect(20, 10), Rectangle(60, 0, 20, 10))
        self.assertEqual(s.add_rect(100, 50), Rectangle(0, 50, 100, 50))

        # Next ones only fit if waste is working
        self.assertEqual(s.add_rect(20, 20), Rectangle(40, 30, 20, 20))
        self.assertEqual(s.add_rect(20, 30), Rectangle(60, 10, 20, 30))
        self.assertEqual(s.add_rect(20, 50), Rectangle(80, 0, 20, 50))
        self.assertEqual(s.add_rect(20, 5), Rectangle(60, 40, 20, 5))
        self.assertEqual(s.add_rect(20, 5), Rectangle(60, 45, 20, 5))
        self.assertEqual(s.add_rect(1, 1), None)

    def test_iter(self):
        # Test correctly calculated when waste is enabled
        s = skyline.SkylineBlWm(100, 100)
        self.assertTrue(s.add_rect(50, 50))
        self.assertTrue(s.add_rect(100, 50))
        self.assertEqual(len([r for r in s]), 2)
        self.assertTrue(s.add_rect(40, 40))
        self.assertEqual(len([r for r in s]), 3)

    def test_len(self):
        s = skyline.SkylineBlWm(100, 100)
        self.assertTrue(s.add_rect(50, 50))
        self.assertTrue(s.add_rect(100, 50))
        self.assertEqual(len(s), 2)
        self.assertTrue(s.add_rect(50, 50))
        self.assertEqual(len(s), 3)

    def test_skyline1(self):
        """Test skyline for complex positions is generated correctly
        +---------------------------+
        |                           |
        +---------------------+     |
        |          4          |     |
        +----------------+----+     |
        |       3        |          |
        +----------+-----+    +-----+
        |          |          |     |
        |          |          |  5  |
        |    1     |          |     |
        |          |          |     |
        |          +----------+-----+
        |          |        2       |
        +----------+----------------+
        """
        s = skyline.SkylineMwf(100, 100, rot=False)
        rect1 = s.add_rect(40, 60)
        rect2 = s.add_rect(60, 10)
        rect3 = s.add_rect(70, 20)
        rect4 = s.add_rect(80, 20)
        rect5 = s.add_rect(20, 40)

        self.assertEqual(rect1, Rectangle(0, 0, 40, 60))
        self.assertEqual(rect2, Rectangle(40, 0, 60, 10))
        self.assertEqual(rect3, Rectangle(0, 60, 70, 20))
        self.assertEqual(rect4, Rectangle(0, 80, 80, 20))
        self.assertEqual(rect5, Rectangle(80, 10, 20, 40))

    def test_skyline2(self):
        """
        +---------------------------+
        |                           |
        |                           |
        |      +--------------------+
        |      |         4          |
        |      |                    |
        +----+ +-----------+--------+
        |    |             |        |
        |    |             |        |
        |    |             |        |
        |    |             |        |
        |  1 |             |    3   |
        |    |             |        |
        |    |             |        |
        |    +-------------+        |
        |    |      2      |        |
        +----+-------------+--------+
        """
        s = skyline.SkylineMwfl(100, 100, rot=False)
        rect1 = s.add_rect(20, 60)
        rect2 = s.add_rect(50, 10)
        rect3 = s.add_rect(30, 60)
        rect4 = s.add_rect(70, 20)
    
        self.assertEqual(rect1, Rectangle(0, 0, 20, 60))
        self.assertEqual(rect2, Rectangle(20, 0, 50, 10))
        self.assertEqual(rect3, Rectangle(70, 0, 30, 60))
        self.assertEqual(rect4, Rectangle(30, 60, 70, 20))

    def test_skyline3(self):
        """
        +-------------------+-------+
        |         10        |       |
        +----+----+---------+       |
        |    |    |         |   9   |
        |    | w2 |     8   |       |
        | 6  |    |         |       |
        |    |    +---------+-------+
        |    +----+                 |
        +----+    |         5       |
        |    |  7 +---+-------------+
        |    |    |w1 |             |
        |    +--------+      4      |
        | 1  |        |             |
        |    |    2   +----------+--+
        |    |        |     3    |  |
        +----+--------+----------+--+
        """
        s = skyline.SkylineMwf(100, 100, rot=False)
        rect1 = s.add_rect(20, 50)
        rect2 = s.add_rect(30, 30)
        rect3 = s.add_rect(40, 10)
        rect4 = s.add_rect(50, 40)
        rect5 = s.add_rect(70, 20)
        rect6 = s.add_rect(20, 40)
        rect7 = s.add_rect(10, 30)
        rect8 = s.add_rect(40, 20)
        rect9 = s.add_rect(30, 30)
        rect10 = s.add_rect(70, 10)
        w1 = s.add_rect(20, 20)
        w2 = s.add_rect(10, 30)

        self.assertEqual(rect1, Rectangle(0, 0, 20, 50))
        self.assertEqual(rect2, Rectangle(20, 0, 30, 30))
        self.assertEqual(rect3, Rectangle(50, 0, 40, 10))
        self.assertEqual(rect4, Rectangle(50, 10, 50, 40))
        self.assertEqual(rect5, Rectangle(30, 50, 70, 20))
        self.assertEqual(rect6, Rectangle(0, 50, 20, 40))
        self.assertEqual(rect7, Rectangle(20, 30, 10, 30))
        self.assertEqual(rect8, Rectangle(30, 70, 40, 20))
        self.assertEqual(rect9, Rectangle(70, 70, 30, 30))
        self.assertEqual(rect10, Rectangle(0, 90, 70, 10))
        self.assertEqual(w1, None)
        self.assertEqual(w2, None)
        
        # With Waste management enabled
        s = skyline.SkylineMwfWm(100, 100, rot=False)
        rect1 = s.add_rect(20, 50)
        rect2 = s.add_rect(30, 30)
        rect3 = s.add_rect(40, 10)
        rect4 = s.add_rect(50, 40)
        rect5 = s.add_rect(70, 20)
        rect6 = s.add_rect(20, 40)
        rect7 = s.add_rect(10, 30)
        rect8 = s.add_rect(40, 20)
        rect9 = s.add_rect(30, 30)
        rect10 = s.add_rect(70, 10)
        w1 = s.add_rect(20, 20)
        w2 = s.add_rect(10, 30)

        self.assertEqual(rect1, Rectangle(0, 0, 20, 50))
        self.assertEqual(rect2, Rectangle(20, 0, 30, 30))
        self.assertEqual(rect3, Rectangle(50, 0, 40, 10))
        self.assertEqual(rect4, Rectangle(50, 10, 50, 40))
        self.assertEqual(rect5, Rectangle(30, 50, 70, 20))
        self.assertEqual(rect6, Rectangle(0, 50, 20, 40))
        self.assertEqual(rect7, Rectangle(20, 30, 10, 30))
        self.assertEqual(rect8, Rectangle(30, 70, 40, 20))
        self.assertEqual(rect9, Rectangle(70, 70, 30, 30))
        self.assertEqual(rect10, Rectangle(0, 90, 70, 10))
        self.assertEqual(w1, Rectangle(30, 30, 20, 20))
        self.assertEqual(w2, Rectangle(20, 60, 10, 30))
        
    def test_skyline4(self):
        """
        +---------------------+-----+
        |          4          |  5  |
        |                     |     |
        +----+----------------------+
        |    |                |     |
        |    |                |     |
        |    |                |     |
        |    |       w1       |     |
        |  1 |                |  3  |
        |    |                |     |
        |    |                |     |
        |    |                |     |
        |    +----------------+     |
        |    |                |     |
        |    |       2        |     |
        |    |                |     |
        +----+----------------+-----+
        """
        s = skyline.SkylineMwflWm(100, 100, rot=False)
        rect1 = s.add_rect(20, 80)
        rect2 = s.add_rect(60, 20)
        rect3 = s.add_rect(20, 80)
        rect4 = s.add_rect(80, 20)
        w1 = s.add_rect(60, 50)
        rect5 = s.add_rect(20, 20)

        self.assertEqual(rect1, Rectangle(0, 0, 20, 80))
        self.assertEqual(rect2, Rectangle(20, 0, 60, 20))
        self.assertEqual(rect3, Rectangle(80, 0, 20, 80))
        self.assertEqual(rect4, Rectangle(0, 80, 80, 20))
        self.assertEqual(rect5, Rectangle(80, 80, 20, 20))
        self.assertEqual(w1, Rectangle(20, 20, 60, 50))

    def test_skyline5(self):
        """
        +------+--------------+-----+
        |      |              |     |
        |  8   |       5      |     |
        |      |              |     |
        |      +--------------------+
        +------+              |     |
        |      |              |     |
        |      |       4      |  7  |
        |      |              |     |
        |      |              +-----+
        |  1   +---------+----+     |
        |      |         | w1 |     |
        |      |         |    |  6  |
        |      |    2    +----+     |
        |      |         |  3 |     |
        |      |         |    |     |
        +------+---------+----+-----+
        """
        s = skyline.SkylineMwflWm(100, 100, rot=False)
        rect1 = s.add_rect(20, 70)
        rect2 = s.add_rect(30, 40)
        rect3 = s.add_rect(20, 20)
        rect4 = s.add_rect(50, 40)
        rect5 = s.add_rect(50, 20)
        rect6 = s.add_rect(30, 50)
        rect7 = s.add_rect(20, 30)
        rect8 = s.add_rect(20, 30)
        w1 = s.add_rect(20, 20)

        self.assertEqual(rect1, Rectangle(0, 0, 20, 70))
        self.assertEqual(rect2, Rectangle(20, 0, 30, 40))
        self.assertEqual(rect3, Rectangle(50, 0, 20, 20))
        self.assertEqual(rect4, Rectangle(20, 40, 50, 40))
        self.assertEqual(rect5, Rectangle(20, 80, 50, 20))
        self.assertEqual(rect6, Rectangle(70, 0, 30, 50))
        self.assertEqual(rect7, Rectangle(70, 50, 20, 30))
        self.assertEqual(rect8, Rectangle(0, 70, 20, 30))
        self.assertEqual(w1, Rectangle(50, 20, 20, 20))

    def test_skyline6(self):
        """
        +-------------+-------------+
        |             |             |
        |     4       |             |
        |             +-------------+
        |             |             |
        +-------------*       5     |
        |     3       |             |
        |             |             |
        +-------------+--+----------+
        |                |          |
        |        2       |          |
        |                |          |
        +----------------+----+     |
        |                     |     |
        |          1          |     |
        |                     |     |
        +---------------------+-----+
        """ 
        s = skyline.SkylineMwflWm(100, 100, rot=False)
        rect1 = s.add_rect(80, 30)
        rect2 = s.add_rect(60, 20)
        rect3 = s.add_rect(50, 20)
        rect4 = s.add_rect(50, 30)
        rect5 = s.add_rect(50, 30)

        self.assertEqual(rect1, Rectangle(0, 0, 80, 30))
        self.assertEqual(rect2, Rectangle(0, 30, 60, 20))
        self.assertEqual(rect3, Rectangle(0, 50, 50, 20))
        self.assertEqual(rect4, Rectangle(0, 70, 50, 30))
        self.assertEqual(rect5, Rectangle(50, 50, 50, 30))

    def test_skyline7(self):
        """
        +-----------------+---------+
        +-----------------+         |
        |                 |         |
        |        4        |         |
        |                 |         |
        +-----------+-----+         |
        |           |     |    5    |
        |           |     |         |
        |    w1     |     |         |
        |           |     |         |
        |           |  2  |         |
        |           |     |         |
        +-----------+     +---------+
        |           |     |         |
        |     1     |     |    3    |
        |           |     |         |
        +-----------+-----+---------+
        """
        s = skyline.SkylineMwflWm(100, 100, rot=False)
        rect1 = s.add_rect(40, 20)
        rect2 = s.add_rect(20, 60)
        rect3 = s.add_rect(40, 20)
        rect4 = s.add_rect(60, 20)
        rect5 = s.add_rect(40, 80)
        w1 = s.add_rect(40, 40)

        self.assertEqual(rect1, Rectangle(0, 0, 40, 20))
        self.assertEqual(rect2, Rectangle(40, 0, 20, 60))
        self.assertEqual(rect3, Rectangle(60, 0, 40, 20))
        self.assertEqual(rect4, Rectangle(0, 60, 60, 20))
        self.assertEqual(rect5, Rectangle(60, 20, 40, 80))
        self.assertEqual(w1, Rectangle(0, 20, 40, 40))

    def test_skyline8(self):
        """
        +---------------------------+
        |                           |
        +----------------------+    |
        |           4          |    |
        |                      |    |
        +-----------+-----+----+    |
        |           |     |         |
        |           |     |         |
        |     w1    |     |         |
        |           |     |         |
        |           |  2  |         |
        |           |     |         |
        +-----------+     |         |
        |           |     +---------+
        |     1     |     |     3   |
        |           |     |         |
        +-----------+-----+---------+
        """
        s = skyline.SkylineMwflWm(100, 100, rot=False)
        rect1 = s.add_rect(40, 20)
        rect2 = s.add_rect(20, 60)
        rect3 = s.add_rect(40, 10)
        rect4 = s.add_rect(80, 20)
        w1 = s.add_rect(40, 40)

        self.assertEqual(rect1, Rectangle(0, 0, 40, 20))
        self.assertEqual(rect2, Rectangle(40, 0, 20, 60))
        self.assertEqual(rect3, Rectangle(60, 0, 40, 10))
        self.assertEqual(rect4, Rectangle(0, 60, 80, 20))
        self.assertEqual(w1, Rectangle(0, 20, 40, 40))

    def test_skyline9(self):
        """
        +---------------------------+
        |                           |
        |     +---------------------+
        |     |           4         |
        |     |                     |
        |     +-----+-----+---------+
        |           |     |         |
        |           |     |         |
        |           |     |   w1    |
        |           |     |         |
        |           |  2  |         |
        |           |     |         |
        |           |     +---------+
        |           |     |         |
        +-----------+     |    3    |
        |    1      |     |         |
        +-----------+-----+---------+ 
        """
        s = skyline.SkylineMwflWm(100, 100, rot=False)
        rect1 = s.add_rect(40, 20)
        rect2 = s.add_rect(20, 60)
        rect3 = s.add_rect(40, 30)
        rect4 = s.add_rect(80, 20)
        w1 = s.add_rect(40, 30)

        self.assertEqual(rect1, Rectangle(0, 0, 40, 20))
        self.assertEqual(rect2, Rectangle(40, 0, 20, 60))
        self.assertEqual(rect3, Rectangle(60, 0, 40, 30))
        self.assertEqual(rect4, Rectangle(20, 60, 80, 20))
        self.assertEqual(w1, Rectangle(60, 30, 40, 30))

    def test_skyline10(self):
        """
        +---------------------------+
        |                           |
        |                           |
        |                           |
        |                           |
        |                      +----+
        |                      |    |
        |                      |    |
        |                      |    |
        +----------------+     |    |
        |                |     |    |
        |                +-----+  3 |
        |       1        |     |    |
        |                |  2  |    |
        |                |     |    |
        |                |     |    |
        +----------------+-----+----+
        With rotation
        """
        s = skyline.SkylineMwfl(100, 100, rot=True)
        rect1 = s.add_rect(50, 40)
        rect2 = s.add_rect(30, 30)
        rect3 = s.add_rect(70, 20)
        
        self.assertEqual(rect1, Rectangle(0, 0, 50, 40))
        self.assertEqual(rect2, Rectangle(50, 0, 30, 30))
        self.assertEqual(rect3, Rectangle(80, 0, 20, 70))

    def test_getitem(self): 
        """
        Test __getitem__ works with all rectangles included waste.
        +---------------------------+
        |                           |
        |     +---------------------+
        |     |           4         |
        |     |                     |
        |     +-----+-----+---------+
        |           |     |         |
        |           |     |         |
        |           |     |   w1    |
        |           |     |         |
        |           |  2  |         |
        |           |     |         |
        |           |     +---------+
        |           |     |         |
        +-----------+     |    3    |
        |    1      |     |         |
        +-----------+-----+---------+ 
        """
        s = skyline.SkylineMwflWm(100, 100, rot=False)
        rect1 = s.add_rect(40, 20)
        rect2 = s.add_rect(20, 60)
        rect3 = s.add_rect(40, 30)
        rect4 = s.add_rect(80, 20)
        w1 = s.add_rect(40, 30)

        self.assertEqual(s[0], Rectangle(0, 0, 40, 20))
        self.assertEqual(s[1], Rectangle(40, 0, 20, 60))
        self.assertEqual(s[2], Rectangle(60, 0, 40, 30))
        self.assertEqual(s[3], Rectangle(20, 60, 80, 20))
        self.assertEqual(s[4], Rectangle(60, 30, 40, 30))

        self.assertEqual(s[-1], Rectangle(60, 30, 40, 30))
        self.assertEqual(s[3:], 
                [Rectangle(20, 60, 80, 20), Rectangle(60, 30, 40, 30)])


class TestSkylineMwf(TestCase):

    def test_init(self):
        """ """
        p = skyline.SkylineMwf(100, 100)
        self.assertFalse(p._waste_management)

    def test_fitness(self):
        """Test position wasting less space has better fitness"""
        p = skyline.SkylineMwf(100, 100, rot=False)
        p.add_rect(20, 20)

        self.assertTrue(p.fitness(90, 10) < p.fitness(100, 10))

    def test_skyline(self):
        """
        +---------------------------+
        |                           |
        |                           |
        +----+   +------------------+
        |    |   |         5        |
        |    |   +---+--+-----------+
        |    |       |  |           |
        |    |       |  |           |
        |    |       |  |           |
        | 1  |       |  |           |
        |    |       |  +-----------+
        |    +-------+ 3|           |
        |    |       |  |           |
        |    |       |  |     4     |
        |    |   2   |  |           |
        |    |       |  |           |
        +----+-------+--+-----------+
        """
        s = skyline.SkylineMwf(100, 100, rot=False)
        rect1 = s.add_rect(20, 80)
        rect2 = s.add_rect(20, 40)
        rect3 = s.add_rect(20, 70)
        rect4 = s.add_rect(40, 50)
        rect5 = s.add_rect(70, 10)

        self.assertEqual(rect1, Rectangle(0, 0, 20, 80))
        self.assertEqual(rect2, Rectangle(20, 0, 20, 40))
        self.assertEqual(rect3, Rectangle(40, 0, 20, 70))
        self.assertEqual(rect4, Rectangle(60, 0, 40, 50))
        self.assertEqual(rect5, Rectangle(30, 70, 70, 10))



class TestSkylineMwFwm(TestCase):

    def test_init(self):
        """Test Waste management is enabled"""
        p = skyline.SkylineMwfWm(100, 100)
        self.assertTrue(p._waste_management)

    def test_skyline(self):
        """
        +---------------------------+
        |                           |
        |                           |
        +----+   +------------------+
        |    |   |         5        |
        |    |   +---+--+-----------+
        |    |       |  |           |
        |    |       |  |           |
        |    |       |  |    w1     |
        | 1  |       |  |           |
        |    |       |  +-----------+
        |    +-------+ 3|           |
        |    |       |  |           |
        |    |       |  |     4     |
        |    |   2   |  |           |
        |    |       |  |           |
        +----+-------+--+-----------+
        """
        s = skyline.SkylineMwfWm(100, 100, rot=False)
        rect1 = s.add_rect(20, 80)
        rect2 = s.add_rect(20, 40)
        rect3 = s.add_rect(20, 70)
        rect4 = s.add_rect(40, 50)
        rect5 = s.add_rect(70, 10)
        w1 = s.add_rect(40, 20)

        self.assertEqual(rect1, Rectangle(0, 0, 20, 80))
        self.assertEqual(rect2, Rectangle(20, 0, 20, 40))
        self.assertEqual(rect3, Rectangle(40, 0, 20, 70))
        self.assertEqual(rect4, Rectangle(60, 0, 40, 50))
        self.assertEqual(rect5, Rectangle(30, 70, 70, 10))
        self.assertEqual(w1, Rectangle(60, 50, 40, 20))



class TestSkylineMwfl(TestCase):

    def test_init(self):
        """ """
        p = skyline.SkylineMwfl(100, 100)
        self.assertFalse(p._waste_management)
    
    def test_fitness(self):
        """Test lower one has best fitness"""
        p = skyline.SkylineMwfl(100, 100, rot=False)
        p.add_rect(20, 20)

        self.assertTrue(p.fitness(90, 10) < p.fitness(90, 20))

    def test_skyline1(self):
        """
        +---------------------------+
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        |                  +--------+
        +------------------+    3   |
        |                  |        |
        |                  +--------+
        |                  |        |
        |        1         |        |
        |                  |    2   |
        |                  |        |
        |                  |        |
        +------------------+--------+
        """
        s = skyline.SkylineMwfl(100, 100, rot=True)
        rect1 = s.add_rect(70, 50)
        rect2 = s.add_rect(40, 30)
        rect3 = s.add_rect(20, 30)

        self.assertEqual(rect1, Rectangle(0, 0, 70, 50))
        self.assertEqual(rect2, Rectangle(70, 0, 30, 40))
        self.assertEqual(rect3, Rectangle(70, 40, 30, 20))

    def test_skyline2(self):
        """
        +---------------------------+
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        +-----------+---------------+
        |           |       3       |
        |           |               |
        |     1     +---------+-----+
        |           |    2    |     |
        |           |         |     |
        +-----------+---------+-----+
        """
        s = skyline.SkylineMwfl(100, 100, rot=False)
        rect1 = s.add_rect(40, 40)
        rect2 = s.add_rect(40, 20)
        rect3 = s.add_rect(60, 20)

        self.assertEqual(rect1, Rectangle(0, 0, 40, 40))
        self.assertEqual(rect2, Rectangle(40, 0, 40, 20))
        self.assertEqual(rect3, Rectangle(40, 20, 60, 20))



class TestSkylineMwflWm(TestCase):

    def test_init(self):
        """Test Waste management is enabled"""
        p = skyline.SkylineMwflWm(100, 100)
        self.assertTrue(p._waste_management)

    def test_skyline(self):
        """
        +---------------------------+
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        +-----------+---------------+
        |           |       3       |
        |           |               |
        |     1     +---------+-----+
        |           |    2    |  w1 |
        |           |         |     |
        +-----------+---------+-----+
        """
        s = skyline.SkylineMwflWm(100, 100, rot=False)
        rect1 = s.add_rect(40, 40)
        rect2 = s.add_rect(40, 20)
        rect3 = s.add_rect(60, 20)
        w1 = s.add_rect(20, 20)

        self.assertEqual(rect1, Rectangle(0, 0, 40, 40))
        self.assertEqual(rect2, Rectangle(40, 0, 40, 20))
        self.assertEqual(rect3, Rectangle(40, 20, 60, 20))
        self.assertEqual(w1, Rectangle(80, 0, 20, 20))



class TestSkylineBl(TestCase):

    def test_init(self):
        """Test Waste management is disabled"""
        p = skyline.SkylineBl(100, 100)
        self.assertFalse(p._waste_management)

    def test_fitness(self):
        """Test lower is better"""
        p = skyline.SkylineBl(100, 100, rot=False)
        self.assertEqual(p.fitness(100, 20), p.fitness(10, 20))
        self.assertTrue(p.fitness(100, 10) < p.fitness(100, 11))

        # The same but with wasted space
        p = skyline.SkylineBl(100, 100, rot=False)
        p.add_rect(80, 50)
        self.assertEqual(p.fitness(100, 10), p.fitness(80, 10))
        self.assertTrue(p.fitness(100, 10) < p.fitness(40, 20))

    def test_skyline1(self):
        """
        +---------------------------+
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        +-------------+-------------+
        |      4      |             |
        |             |             |
        +---------+---+             |
        |         |   |      3      |
        |         |   |             |
        |    1    +---+             |
        |         | 2 |             |
        |         |   |             |
        +---------+---+-------------+
        
        Test lower positions is better than one not losing space
        """
        s = skyline.SkylineBl(100, 100, rot=False)
        rect1 = s.add_rect(40, 30)
        rect2 = s.add_rect(10, 20)
        rect3 = s.add_rect(50, 50)
        rect4 = s.add_rect(50, 20)

        self.assertEqual(rect1, Rectangle(0, 0, 40, 30))
        self.assertEqual(rect2, Rectangle(40, 0, 10, 20))
        self.assertEqual(rect3, Rectangle(50, 0, 50, 50))
        self.assertEqual(rect4, Rectangle(0, 30, 50, 20))

    def test_skyline2(self):
        """
        +---------------------------+
        |                           |
        |                           |
        |                           |
        +--------------------+      |
        |                    |      |
        |         4          +------+
        |                    |  5   |
        |                    |      |
        +----------------+---+------+
        |                |     3    |
        |                |          |
        |       1        +-----+----+
        |                |  2  |    |
        |                |     |    |
        +----------------+-----+----+
        """
        s = skyline.SkylineBl(100, 100, rot=False)
        rect1 = s.add_rect(50, 40)
        rect2 = s.add_rect(30, 20)
        rect3 = s.add_rect(50, 20)
        rect4 = s.add_rect(70, 30)
        rect5 = s.add_rect(20, 20)
   
        self.assertEqual(rect1, Rectangle(0, 0, 50, 40))
        self.assertEqual(rect2, Rectangle(50, 0, 30, 20))
        self.assertEqual(rect3, Rectangle(50, 20, 50, 20))
        self.assertEqual(rect4, Rectangle(0, 40, 70, 30))
        self.assertEqual(rect5, Rectangle(70, 40, 20, 20))


class TestSkylineBlWm(TestCase):

    def test_init(self):
        """Test Waste management is enabled"""
        p = skyline.SkylineBlWm(100, 100)
        self.assertTrue(p._waste_management)

    def test_skyline1(self):
        """
        +---------------------------+
        |                           |
        |                           |
        |                           |
        |                           |
        +--------------------+      |
        |                    |      |
        |         4          |      |
        |                    |      |
        |                    |      |
        +----------------+---+------+
        |                |     3    |
        |                |          |
        |       1        +-----+----+
        |                |  2  | w1 |
        |                |     |    |
        +----------------+-----+----+
        """
        s = skyline.SkylineBlWm(100, 100, rot=False)
        rect1 = s.add_rect(50, 40)
        rect2 = s.add_rect(30, 20)
        rect3 = s.add_rect(50, 20)
        rect4 = s.add_rect(70, 30)
        w1 = s.add_rect(20, 20)
   
        self.assertEqual(rect1, Rectangle(0, 0, 50, 40))
        self.assertEqual(rect2, Rectangle(50, 0, 30, 20))
        self.assertEqual(rect3, Rectangle(50, 20, 50, 20))
        self.assertEqual(rect4, Rectangle(0, 40, 70, 30))
        self.assertEqual(w1, Rectangle(80, 0, 20, 20))
        

