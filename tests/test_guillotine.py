from unittest import TestCase
import rectpack.guillotine as guillotine
from rectpack.geometry import Rectangle


class TestGuillotine(TestCase):

    def test_init(self):
        # Test default section
        g = guillotine.Guillotine(100, 100)
        self.assertEqual(len(g._sections), 1)
        self.assertEqual(g._sections[0], Rectangle(0, 0, 100, 100))

        # Test arguments
        g = guillotine.Guillotine(50, 100)
        self.assertEqual(g.width, 50)
        self.assertEqual(g.height, 100)

        # Test merge optional argument
        g = guillotine.Guillotine(50, 100)
        self.assertEqual(g._merge, True)
        g = guillotine.Guillotine(50, 100, merge=False)
        self.assertEqual(g._merge, False)
        g = guillotine.Guillotine(50, 100, merge=True)
        self.assertEqual(g._merge, True)

    def test_add_rect(self):
        # Rectangle too big for surface
        g = guillotine.GuillotineBssfMaxas(100, 100, merge=False)
        self.assertEqual(g.add_rect(110, 3), None)
        
        g = guillotine.GuillotineBssfMaxas(100, 100, merge=False)
        self.assertEqual(g.add_rect(5, 5), Rectangle(0, 0, 5, 5))
        self.assertEqual(len(g), 1)
        self.assertTrue(g.add_rect(10, 10))
        self.assertEqual(len(g), 2)
        self.assertEqual(g.add_rect(99, 99), None)
        self.assertEqual(len(g), 2)

        # Test new sections created
        g = guillotine.GuillotineBssfMaxas(100, 100)
        self.assertEqual(len(g._sections), 1)
        g.add_rect(5, 5)
        self.assertEqual(len(g._sections), 2)

        # Test rectangle id preserved
        g = guillotine.GuillotineBssfMaxas(100, 100)
        g.add_rect(5, 5, rid=88)
        for r in g:
            self.assertEqual(r.rid, 88)

        # Test full size rectangle
        g = guillotine.GuillotineBssfMaxas(300, 100)
        self.assertTrue(g.add_rect(300, 100))

        # Test rotations
        g = guillotine.GuillotineBlsfMaxas(50, 100, rot=True)
        rect = g.add_rect(100, 50)
        self.assertEqual(rect, Rectangle(0, 0, 50, 100))

        # Test returned coordinates
        g = guillotine.GuillotineBlsfMaxas(100, 100, rot=False)
        rect1 = g.add_rect(60, 40)
        rect2 = g.add_rect(20, 30)
        rect3 = g.add_rect(30, 40)
        self.assertEqual(rect1, Rectangle(0, 0, 60, 40))
        self.assertEqual(rect2, Rectangle(0, 40, 20, 30))
        self.assertEqual(rect3, Rectangle(60, 0, 30, 40))

    def test_fitness(self):
        # Test several sections same fitness value
        g = guillotine.GuillotineBlsfMaxas(50, 50, rot=False)
        fitness1 = g.fitness(10, 10)
        fitness2 = g.fitness(20, 20)
        fitness3 = g.fitness(30, 30)
        fitness4 = g.fitness(40, 40)
        fitness5 = g.fitness(45, 45)
        self.assertTrue(fitness1>fitness2>fitness3>fitness4>fitness5)
        g.add_rect(5, 5)
        fitness1 = g.fitness(10, 10)
        fitness2 = g.fitness(20, 20)
        fitness3 = g.fitness(30, 30)
        fitness4 = g.fitness(40, 40)
        fitness5 = g.fitness(45, 45)
        self.assertTrue(fitness1>fitness2>fitness3>fitness4>fitness5)

    def test_section_fitness(self):
        g1 = guillotine.GuillotineBssfSas(100, 50)
        g2 = guillotine.GuillotineBlsfSas(100, 50)
        g3 = guillotine.GuillotineBafSas(100, 50)
        
        fit1 = g1._section_fitness(g1._sections[0], 5, 6)
        fit2 = g2._section_fitness(g2._sections[0], 5, 6)
        fit3 = g3._section_fitness(g3._sections[0], 5, 6)
        self.assertNotEqual(fit1, fit2, fit3)

    def test_split_vertical(self):
        # Normal split
        g = guillotine.Guillotine(100, 100)

        section = g._sections[0]
        g._sections = []
        g._split_vertical(section, 50, 50)
        
        self.assertTrue(Rectangle(50, 0, 50, 100) in g._sections)
        self.assertTrue(Rectangle(0, 50, 50, 50) in g._sections)
        self.assertEqual(len(g._sections), 2)

        # Full width split
        g = guillotine.Guillotine(100, 100)

        section = g._sections[0]
        g._sections = []
        g._split_vertical(section, 100, 50)
        
        self.assertTrue(Rectangle(0, 50, 100, 50) in g._sections)
        self.assertEqual(len(g._sections), 1)

        # Full Height split
        g = guillotine.Guillotine(100, 100)

        section = g._sections[0]
        g._sections = []
        g._split_vertical(section, 50, 100)
       
        self.assertTrue(Rectangle(50, 0, 50, 100) in g._sections)
        self.assertEqual(len(g._sections), 1)

        # Full section split
        g = guillotine.Guillotine(100, 100)

        section = g._sections[0]
        g._sections = []
        g._split_vertical(section, 100, 100)
        
        self.assertEqual(len(g._sections), 0)
      
    def test_split_horizontal(self):
        # Normal split
        g = guillotine.Guillotine(100, 100)

        section = g._sections[0]
        g._sections = []
        g._split_horizontal(section, 50, 50)

        self.assertTrue(Rectangle(0, 50, 100, 50) in g._sections)
        self.assertTrue(Rectangle(50, 0, 50, 50) in g._sections)
        self.assertEqual(len(g._sections), 2)

        # Full width split
        g = guillotine.Guillotine(100, 100)

        section = g._sections[0]
        g._sections = []
        g._split_horizontal(section, 100, 50)

        self.assertTrue(Rectangle(0, 50, 100, 50) in g._sections)
        self.assertEqual(len(g._sections), 1)

        # Full height split
        g = guillotine.Guillotine(100, 100)

        section = g._sections[0]
        g._sections = []
        g._split_horizontal(section, 50, 100)

        self.assertTrue(Rectangle(50, 0, 50, 100) in g._sections)
        self.assertEqual(len(g._sections), 1)
        
        # Full section split
        g = guillotine.Guillotine(100, 100)

        section = g._sections[0]
        g._sections = []
        g._split_horizontal(section, 100, 100)

        self.assertEqual(len(g._sections), 0)

    def test_split(self):
        #TODO: Test correct split is called for each subclass
        pass

    def test_fits_surface(self):
        g = guillotine.Guillotine(100, 200, rot=False)
        self.assertTrue(g._fits_surface(10, 10))
        self.assertTrue(g._fits_surface(100, 200))
        self.assertTrue(g._fits_surface(100, 100))
        self.assertFalse(g._fits_surface(101, 200))
        self.assertFalse(g._fits_surface(100, 201))

    def test_add_section(self):
        g = guillotine.Guillotine(100, 100)
        g._sections = [Rectangle(0, 50, 50, 50)]
        g._add_section(Rectangle(50, 0, 50, 50))

        self.assertEqual(len(g._sections), 2)

        # Test sections are merged recursively
        g = guillotine.Guillotine(100, 100, merge=True)
        g._sections = [Rectangle(0, 50, 100, 50), Rectangle(50, 0, 50, 50)]

        g._add_section(Rectangle(0, 0, 50, 50))

        self.assertEqual(len(g._sections), 1)
        self.assertEqual(g._sections[0], Rectangle(0, 0, 100, 100))

        # Test merge disabled
        g = guillotine.Guillotine(100, 100, merge=False)
        g._sections = [Rectangle(0, 50, 100, 50), Rectangle(50, 0, 50, 50)]
        
        g._add_section(Rectangle(0, 0, 50, 50))
        self.assertEqual(len(g._sections), 3)                
        self.assertTrue(Rectangle(0, 50, 100, 50) in g._sections)
        self.assertTrue(Rectangle(50, 0, 50, 50) in g._sections)
        self.assertTrue(Rectangle(0, 0, 50, 50) in g._sections)

    def test_getitem(self):
        """Test __getitem__ returns requested element or slice"""
        g = guillotine.GuillotineBafSas(100, 100)
        g.add_rect(10, 10)
        g.add_rect(5, 5)
        g.add_rect(1, 1)

        self.assertEqual(g[0], Rectangle(0, 0, 10, 10))
        self.assertEqual(g[1], Rectangle(0, 10, 5, 5))
        self.assertEqual(g[2], Rectangle(5, 10, 1, 1))
        
        self.assertEqual(g[-1], Rectangle(5, 10, 1, 1))
        self.assertEqual(g[-2], Rectangle(0, 10, 5, 5)) 
               
        self.assertEqual(g[1:], 
                [Rectangle(0, 10, 5, 5), Rectangle(5, 10, 1, 1)])
        self.assertEqual(g[0:2],
                [Rectangle(0, 0, 10, 10), Rectangle(0, 10, 5, 5)])
