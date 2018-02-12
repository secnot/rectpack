import random 
from unittest import TestCase
from collections import defaultdict
from timeit import default_timer as timer
import rectpack


from  rectpack import GuillotineBssfSas, GuillotineBssfLas, \
    GuillotineBssfSlas, GuillotineBssfLlas, GuillotineBssfMaxas, \
    GuillotineBssfMinas, GuillotineBlsfSas, GuillotineBlsfLas, \
    GuillotineBlsfSlas, GuillotineBlsfLlas, GuillotineBlsfMaxas, \
    GuillotineBlsfMinas, GuillotineBafSas, GuillotineBafLas, \
    GuillotineBafSlas, GuillotineBafLlas, GuillotineBafMaxas, \
    GuillotineBafMinas

from rectpack import MaxRectsBl, MaxRectsBssf, MaxRectsBaf, MaxRectsBlsf

from rectpack import SkylineMwf, SkylineMwfl, SkylineBl, \
    SkylineBlWm, SkylineMwfWm, SkylineMwflWm

from rectpack import PackingMode, PackingBin


# For repeatable rectangle generation
random.seed(33)


def coherce_to(maxn, minn, n):
    assert maxn >= minn
    return max(min(maxn, n), minn)


def random_rectangle(max_side, min_side, sigma=0.5, ratio=1.0, coherce=True):

    assert min_side <= max_side

    #
    half_side = (max_side-min_side)/2
    center = max_side-half_side
    width  = random.normalvariate(0, sigma)*half_side
    height = random.normalvariate(0, sigma)*half_side

    #
    if ratio > 1:
        height = height/ratio
    else:
        width = width*ratio
   
    # Coherce value to max
    if coherce:
        width  = coherce_to(max_side, min_side, width+center)
        height = coherce_to(max_side, min_side, height+center)
    
    return width, height


RECTANGLES = [random_rectangle(40, 20, ratio=1.2) for _ in range(50)]\
        +[random_rectangle(20, 15, ratio=1.2) for _ in range(50)]
BINS = [random_rectangle(150, 150, ratio=1.5) for _ in range(3)]


class TestWastedSpace(TestCase):

    def setUp(self):
        self.rectangles = [(int(w), int(h)) for w, h in RECTANGLES]
        self.bins = [(int(w), int(h)) for w, h in BINS]
        self.packer = None
        self.algos = [
            GuillotineBssfSas, GuillotineBssfLas, GuillotineBssfSlas, \
            GuillotineBssfLlas, GuillotineBssfMaxas, GuillotineBssfMinas, \
            GuillotineBlsfSas, GuillotineBlsfLas, GuillotineBlsfSlas, \
            GuillotineBlsfLlas, GuillotineBlsfMaxas, GuillotineBlsfMinas, \
            GuillotineBafSas, GuillotineBafLas, GuillotineBafSlas, \
            MaxRectsBl, MaxRectsBssf, MaxRectsBaf, MaxRectsBlsf, \
            SkylineBl, SkylineBlWm, SkylineMwfl, SkylineMwf]

        self.bin_algos = [
            (rectpack.PackingBin.BNF, "BNF"),
            (rectpack.PackingBin.BFF, "BFF"),
            (rectpack.PackingBin.BBF, "BBF"),
            (rectpack.PackingBin.Global, "GLOBAL"),
        ] 
        self.bin_algos_online = [
            (rectpack.PackingBin.BNF, "BNF"),
            (rectpack.PackingBin.BFF, "BFF"),
            (rectpack.PackingBin.BBF, "BBF"),
        ] 
        self.sort_algo = rectpack.SORT_AREA
        self.log=False

    @staticmethod
    def first_bin_wasted_space(packer):
        bin1 = packer[1] 
        bin_area = bin1.width*bin1.height
        rect_area = sum((r.width*r.height for r in bin1))    
        return ((bin_area-rect_area)/bin_area)*100


    @staticmethod
    def packing_time(packer):
        start = timer()
        packer.pack()
        end = timer()
        return end-start

    @staticmethod
    def setup_packer(packer, bins, rectangles):
        for b in bins:
            packer.add_bin(*b)
        for r in rectangles:
            packer.add_rect(*r)
        return packer

    def test_offline_modes(self):
        for bin_algo, algo_name in self.bin_algos:
            for algo in self.algos:
                packer = rectpack.newPacker(pack_algo=algo, 
                        mode=PackingMode.Offline, 
                        bin_algo=bin_algo,
                        sort_algo=self.sort_algo)
                self.setup_packer(packer, self.bins, self.rectangles)
                time = self.packing_time(packer)
                self.first_bin_wasted_space(packer)
                wasted = self.first_bin_wasted_space(packer)

                # Test wasted spaced threshold
                if self.log:
                    print("Offline {0} {1:<20s} {2:>10.3f}s {3:>10.3f}% {4:>10} bins".format(
                        algo_name, algo.__name__, time, wasted, len(packer)))
                self.assertTrue(wasted<50)

                # Validate rectangle packing
                for b in packer:
                    b.validate_packing()

    def test_online_modes(self):
        for bin_algo, algo_name in self.bin_algos_online:
            for algo in self.algos:
                packer = rectpack.newPacker(pack_algo=algo, 
                        mode=PackingMode.Online, 
                        bin_algo=bin_algo,
                        sort_algo=self.sort_algo)
                start = timer()
                self.setup_packer(packer, self.bins, self.rectangles)
                end = timer()
                time = end-start
                self.first_bin_wasted_space(packer)
                wasted = self.first_bin_wasted_space(packer)

                # Test wasted spaced threshold
                if self.log:
                    print("Online {0} {1:<20s} {2:>10.3f}s {3:>10.3f}% {4:>10} bins".format(
                        algo_name, algo.__name__, time, wasted, len(packer)))
                self.assertTrue(wasted<90)

                # Validate rectangle packing
                for b in packer:
                    b.validate_packing()




