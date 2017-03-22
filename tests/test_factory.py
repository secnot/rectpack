from unittest import TestCase
from rectpack.packer import newPacker, PackingMode, PackingBin
import random


class TestFactory(TestCase):
    
    def setUp(self):
        self.rectangles = [(w, h) for w in range(8, 50, 8) for h in range(8, 50, 8)]

    def _common(self, mode, bin_algo, width, height):
        # create a new packer
        p = newPacker(mode, bin_algo)
        # as many bins as rectangles should be enough
        p.add_bin(width, height, count=len(self.rectangles))
        # try to add the rectangles
        for r in self.rectangles:
            p.add_rect(*r)
        # pack them, if in offline mode
        if mode == PackingMode.Offline:
            p.pack()
        # provide the results for validation
        return p

    def test_Offline_BNF_big_enough(self):
        # create bins that are big enough to hold the rectangles
        p = self._common(PackingMode.Offline, PackingBin.BNF, 50, 50)
        # check that bins were created
        self.assertGreater(len(p.bin_list()), 0)
        # check that all of the rectangles made it in
        self.assertEqual(len(p.rect_list()), len(self.rectangles))

    def test_Offline_BNF_too_small(self):
        # create bins that are too small to hold the rectangles
        p = self._common(PackingMode.Offline, PackingBin.BNF, 5, 5)
        # check that none of the rectangles made it in
        self.assertEqual(len(p.rect_list()), 0)

    def test_Offline_BFF_big_enough(self):
        # create bins that are big enough to hold the rectangles
        p = self._common(PackingMode.Offline, PackingBin.BFF, 50, 50)
        # check that bins were created
        self.assertGreater(len(p.bin_list()), 0)
        # check that all of the rectangles made it in
        self.assertEqual(len(p.rect_list()), len(self.rectangles))

    def test_Offline_BFF_too_small(self):
        # create bins that are too small to hold the rectangles
        p = self._common(PackingMode.Offline, PackingBin.BFF, 5, 5)
        # check that none of the rectangles made it in
        self.assertEqual(len(p.rect_list()), 0)

    def test_Offline_BBF_big_enough(self):
        # create bins that are big enough to hold the rectangles
        p = self._common(PackingMode.Offline, PackingBin.BBF, 50, 50)
        # check that bins were created
        self.assertGreater(len(p.bin_list()), 0)
        # check that all of the rectangles made it in
        self.assertEqual(len(p.rect_list()), len(self.rectangles))

    def test_Offline_BBF_too_small(self):
        # create bins that are too small to hold the rectangles
        p = self._common(PackingMode.Offline, PackingBin.BBF, 5, 5)
        # check that none of the rectangles made it in
        self.assertEqual(len(p.rect_list()), 0)

    def test_Offline_Global_big_enough(self):
        # create bins that are big enough to hold the rectangles
        p = self._common(PackingMode.Offline, PackingBin.Global, 50, 50)
        # check that bins were created
        self.assertGreater(len(p.bin_list()), 0)
        # check that all of the rectangles made it in
        self.assertEqual(len(p.rect_list()), len(self.rectangles))

    def test_Offline_Global_too_small(self):
        # create bins that are too small to hold the rectangles
        p = self._common(PackingMode.Offline, PackingBin.Global, 5, 5)
        # check that none of the rectangles made it in
        self.assertEqual(len(p.rect_list()), 0)


def helper():
    """create a bunch of tests to copy and paste into TestFactory"""
    for mode in PackingMode:
        for bin_algo in PackingBin:
            for size, w, h in ('big_enough', 50, 50), ('too_small', 5, 5):
                name = '_'.join(('test', mode, bin_algo, size))
                print("""\
    def %s(self):
        # create bins that are %s to hold the rectangles
        p = self._common(PackingMode.%s, PackingBin.%s, %s, %s)""" %
                      (name, size.replace('_', ' '), mode, bin_algo, w, h))
                if size == 'big_enough':
                    print("""\
        # check that bins were created
        self.assertGreater(len(p.bin_list()), 0)
        # check that all of the rectangles made it in
        self.assertEqual(len(p.rect_list()), len(self.rectangles))
""")
                else:
                    print("""\
        # check that none of the rectangles made it in
        self.assertEqual(len(p.rect_list()), 0)
""")
