from unittest import TestCase
import rectpack.waste as waste
from rectpack.geometry import Rectangle

class TestWaste(TestCase):

    def test_init(self):
        w = waste.WasteManager()

    def test_add_waste(self):
        w = waste.WasteManager()
        w.add_waste(30, 40, 50, 50)
        w.add_waste(5, 5, 20, 20)
        w.add_waste(0, 100, 100, 100)

        rect1 = w.add_rect(20, 20)
        rect2 = w.add_rect(45, 40)
        rect3 = w.add_rect(90, 80)
        rect4 = w.add_rect(100, 100)
        rect5 = w.add_rect(10, 10)
            
        self.assertEqual(rect1, Rectangle(5, 5, 20, 20))
        self.assertEqual(rect2, Rectangle(30, 40, 45, 40))
        self.assertEqual(rect3, Rectangle(0, 100, 90, 80))
        self.assertEqual(rect4, None)
        self.assertEqual(rect5, Rectangle(30, 80, 10, 10))
        
        self.assertEqual(len(w), 4)

        # Test merge is enabled for new waste 
        w = waste.WasteManager()
        w.add_waste(0, 0, 50, 50)
        w.add_waste(50, 0, 50, 50)
        self.assertEqual(len(w._sections), 1)
        self.assertEqual(w.add_rect(100, 50), Rectangle(0, 0, 100, 50))

    def test_empty(self):
        # Test it is empty by default
        w = waste.WasteManager()
        self.assertFalse(w.add_rect(1, 1), None)

    def test_add_rect(self):
        w = waste.WasteManager(rot=False)
        w.add_waste(50, 40, 100, 40)
        self.assertEqual(w.add_rect(30, 80), None)

        # Test with rotation
        w = waste.WasteManager(rot=True)
        w.add_waste(50, 40, 100, 40)
        self.assertEqual(w.add_rect(30, 80), Rectangle(50, 40, 80, 30))

        # Test rectangle rid
        w = waste.WasteManager(rot=True)
        w.add_waste(50, 40, 100, 40)
        rect = w.add_rect(30, 80, rid=23)
        self.assertEqual(rect.rid, 23)
   

    def test_iter(self):
        # Iterate through rectangles
        w = waste.WasteManager()
        w.add_waste(30, 40, 50, 50)
        w.add_waste(5, 5, 20, 20)
        w.add_waste(0, 100, 100, 100)

        w.add_rect(50, 50)

        for r in w:
            self.assertEqual(r, Rectangle(30, 40, 50, 50))

        self.assertEqual(len(w), 1)
