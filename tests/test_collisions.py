from unittest import TestCase
import random

import rectpack.guillotine as guillotine
import rectpack.skyline as skyline
import rectpack.maxrects as maxrects
import rectpack.packer as packer


def random_rectangle(max_side, min_side):
    width = random.randint(min_side, max_side)
    height = random.randint(min_side, max_side)     
    return (width, height)


def random_rectangle_generator(num, max_side=30, min_side=8):
    """
    Generate a random rectangle list with dimensions within
    specified parameters.

    Arguments:
        max_dim (number): Max rectangle side length
        min_side (number): Min rectangle side length
        max_ratio (number):

    Returns:
        Rectangle list
    """
    return (random_rectangle(max_side, min_side) for i in range(0, num))



class TestCollisions(TestCase):

    def setUp(self):
        self.rectangles = [r for r in random_rectangle_generator(1000)]
        self.bins = [(100, 100, 1), (150, 150, 20)]

    def setup_packer(self, packer):
        for b in self.bins:
            packer.add_bin(b[0], b[1], b[2])

        for r in self.rectangles:
            packer.add_rect(r[0], r[1])

    def test_maxrects_bl(self):
        m = packer.PackerBBF(pack_algo=maxrects.MaxRectsBl, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(m)
        m.pack()
        m.validate_packing()
     
    def test_maxrects_bssf(self):
        m = packer.PackerBBF(pack_algo=maxrects.MaxRectsBssf, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(m)
        m.pack() 
        m.validate_packing()
        
    def test_maxrects_baf(self):
        m = packer.PackerBBF(pack_algo=maxrects.MaxRectsBaf, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(m)
        m.pack()
        m.validate_packing()

    def test_maxrects_blsf(self):
        m = packer.PackerBBF(pack_algo=maxrects.MaxRectsBlsf, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(m)
        m.pack()
        m.validate_packing()
         
    def test_skyline_bl_wm(self):
        s = packer.PackerBBF(pack_algo=skyline.SkylineBlWm, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(s)
        s.pack()
        s.validate_packing()

    def test_skyline_mwf_wm(self):
        s = packer.PackerBBF(pack_algo=skyline.SkylineMwfWm, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(s)
        s.pack()
        s.validate_packing()

    def test_skyline_mwfl_wm(self):
        s = packer.PackerBBF(pack_algo=skyline.SkylineMwflWm, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(s)
        s.pack()
        s.validate_packing()
         
    def test_skyline_bl(self):
        s = packer.PackerBBF(pack_algo=skyline.SkylineBl, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(s)
        s.pack()
        s.validate_packing()

    def test_skyline_mwf(self):
        s = packer.PackerBBF(pack_algo=skyline.SkylineMwf, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(s)
        s.pack()
        s.validate_packing()

    def test_skyline_mwfl(self):
        s = packer.PackerBBF(pack_algo=skyline.SkylineMwfl, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(s)
        s.pack()
        s.validate_packing()

    def test_guillotine_bssf_sas(self): 
        g = packer.PackerBBF(pack_algo=guillotine.GuillotineBssfSas, 
                sort_algo=packer.SORT_SSIDE, rotation=True)
        self.setup_packer(g)
        g.pack()
        g.validate_packing()

    def test_guillotine_blsf_las(self): 
        g = packer.PackerBBF(pack_algo=guillotine.GuillotineBlsfLas, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(g)
        g.pack()
        g.validate_packing()
 
    def test_guillotine_baf_slas(self): 
        g = packer.PackerBBF(pack_algo=guillotine.GuillotineBafSlas, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(g)
        g.pack()
        g.validate_packing()

    def test_guillotine_bssf_llas(self): 
        g = packer.PackerBBF(pack_algo=guillotine.GuillotineBssfLlas, 
                sort_algo=packer.SORT_SSIDE, rotation=True)
        self.setup_packer(g)
        g.pack()
        g.validate_packing()

    def test_guillotine_blsf_maxas(self): 
        g = packer.PackerBBF(pack_algo=guillotine.GuillotineBlsfMaxas, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(g)
        g.pack()
        g.validate_packing()
 
    def test_guillotine_baf_minas(self): 
        g = packer.PackerBBF(pack_algo=guillotine.GuillotineBafMinas, 
                sort_algo=packer.SORT_LSIDE, rotation=True)
        self.setup_packer(g)
        g.pack()
        g.validate_packing()

