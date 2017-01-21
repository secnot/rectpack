from unittest import TestCase
import rectpack.packer
import random


class TestGenerator(TestCase):
    
    def setUp(self):
        self.rectangles = [(w, h) for w in range(8,50, 8) for h in range(8,50, 8)]

    def test_factory(self):
        p = rectpack.packer.newPacker()
        for r in self.rectangles:
            p.add_rect(*r)
        p.add_factory(50, 50)
        p.pack()
        # check that bins were generated
        self.assertGreater(len(p.bin_list()), 0)
        # check that all of the rectangles made it in
        self.assertEqual(len(p.rect_list()), len(self.rectangles))
