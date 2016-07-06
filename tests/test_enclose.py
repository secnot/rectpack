from unittest import TestCase
import rectpack.enclose as enclose
import random



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



class TestEnclose(TestCase):
    
    def setUp(self):
        from math import sqrt, ceil
        self.rectangles = [r for r in random_rectangle_generator(100)]
        self.area = sum(r[0]*r[1] for r in self.rectangles)
        self.max_width = ceil(sqrt(self.area)*1.20)
        self.max_height = ceil(sqrt(self.area)*1.80)

    def test_container_candidates(self):
        # Test without rotation
        en = enclose.Enclose(rotation=False)
        en.add_rect(2, 100)
        en.add_rect(3, 100)
        candidates = en._container_candidates()

        self.assertTrue((5, 200) in candidates)
        self.assertTrue((3, 200) in candidates)
        self.assertFalse((2, 200) in candidates)
 
        # Test with rotation
        en = enclose.Enclose(rotation=True)
        en.add_rect(2, 100)
        en.add_rect(3, 100)
        candidates = en._container_candidates()

        self.assertTrue((100, 200) in candidates)
        self.assertTrue((200, 200) in candidates)
        self.assertTrue((105, 200) in candidates)

        # Width limit
        en = enclose.Enclose(max_width=180)
        en.add_rect(2, 100)
        en.add_rect(3, 100)
        candidates = en._container_candidates()

        self.assertTrue((100, 200) in candidates)
        self.assertFalse((200, 200) in candidates)

        # Height limit
        en = enclose.Enclose(max_height=180)
        en.add_rect(2, 100)
        en.add_rect(3, 100)
        candidates = en._container_candidates()

        self.assertTrue((3, 180) in candidates)
        self.assertTrue((100, 180) in candidates)
        self.assertTrue((200, 180) in candidates)

    def test_containment(self):
        """
        Test all rectangles are inside the container area
        """
        en = enclose.Enclose(self.rectangles, self.max_width, self.max_height, True)
        packer = en.generate()
       
        # Check all rectangles are inside container
        packer.validate_packing()

    def test_add_rect(self):
        en = enclose.Enclose([], 100, 100, True)
        en.add_rect(10, 10)
        en.add_rect(20, 20)

        packer = en.generate()
        self.assertEqual(packer.width, 30)
        self.assertEqual(packer.height, 20)

        en.add_rect(50, 50)
        packer = en.generate()
        self.assertEqual(packer.width, 50)
        self.assertEqual(packer.height, 70)

    def test_failed_envelope(self):
        """
        Test container not found
        """
        en = enclose.Enclose(self.rectangles, max_width=50, max_height=50)
        packer = en.generate()
        self.assertEqual(packer, None)

        en = enclose.Enclose(max_width=50, max_height=50)
        packer = en.generate()
        self.assertEqual(packer, None)
