from unittest import TestCase
import random
import math
import decimal

from rectpack.guillotine import GuillotineBssfSas
from rectpack.maxrects import MaxRectsBssf
from rectpack.skyline import SkylineMwfWm
from rectpack.packer import PackerBFF, float2dec


def random_rectangle(max_side, min_side):
    width = decimal.Decimal(str(round(random.uniform(max_side, min_side), 1)))
    height = decimal.Decimal(str(round(random.uniform(max_side, min_side), 1)))
    
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


class TestDecimal(TestCase):
    """
    Test all work when using decimal instead of integers
    """
    def setUp(self):
        self.rectangles = [r for r in random_rectangle_generator(500)]
        self.bins = [(80, 80, 1), (100, 100, 30)]

    def setup_packer(self, packer):
        for b in self.bins:
            packer.add_bin(b[0], b[1], b[2])

        for r in self.rectangles:
            packer.add_rect(r[0], r[1])

    def test_maxrects(self):
        m = PackerBFF(pack_algo=MaxRectsBssf, rotation=True)
        self.setup_packer(m)
        m.pack()
        m.validate_packing()
        self.assertTrue(len(m)>1)
        
    def test_guillotine(self):
        g = PackerBFF(pack_algo=GuillotineBssfSas, rotation=True)
        self.setup_packer(g)
        g.pack()
        g.validate_packing()
        self.assertTrue(len(g)>1)
         
    def test_skyline(self):
        s = PackerBFF(pack_algo=SkylineMwfWm, rotation=True)
        self.setup_packer(s)
        s.pack()
        s.validate_packing()
        self.assertTrue(len(s)>1)
    
 
class TestFloat2Dec(TestCase):

    def test_rounding(self):
        """Test rounding is allways up"""
        d = float2dec(3.141511, 3)
        self.assertEqual(decimal.Decimal('3.142'), d)   

        d = float2dec(3.444444, 3)
        self.assertEqual(decimal.Decimal('3.445'), d)

        d = float2dec(3.243234, 0)
        self.assertEqual(decimal.Decimal('4'), d)

        d = float2dec(7.234234, 0)
        self.assertEqual(decimal.Decimal('8'), d)

    def test_decimal_places(self):
        """Test rounded to correct decimal place"""
        d = float2dec(4.2, 3)
        self.assertEqual(decimal.Decimal('4.201'), d)

        d = float2dec(5.7, 3)
        self.assertEqual(decimal.Decimal('5.701'), d)

        d = float2dec(2.2, 4)
        self.assertEqual(decimal.Decimal('2.2001'), d)

    def test_integer(self):
        """Test integers are also converted, but not rounded"""
        d = float2dec(7, 3)
        self.assertEqual(decimal.Decimal('7.000'), d)

        d = float2dec(2, 3)
        self.assertEqual(decimal.Decimal('2.000'), d)

    def test_not_rounded(self):
        """Test floats are only rounded when needed"""
        d = float2dec(3.0, 3)
        self.assertEqual(decimal.Decimal('3.000'), d)
