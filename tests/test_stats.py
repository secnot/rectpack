import random 
from unittest import TestCase
import matplotlib.pyplot as plt
from collections import defaultdict

def coherce_to(maxn, minn, n):
    assert maxn > minn
    return max(min(maxn, n), minn)


def random_rectangle(max_side, min_side, sigma=0.5, ratio=1.0, coherce=True):

    assert min_side < max_side

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


class TestRandomRectangles(TestCase):

    def test_generation(self):
        rects = [random_rectangle(50, 10, ratio=1.5) for _ in range(9900)]

        #average 
        width_avg  = sum((r[0] for r in rects))
        height_avg = sum((r[1] for r in rects))

