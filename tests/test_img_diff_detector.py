import unittest
import numpy as np
import cv2
import src.img_diff_detector as dd

class TestImgDiffDetector(unittest.TestCase):
    def test_identical_images(self):
        img_path = 'data/saizeriya1.jpg'
        actual = dd.calc_diff(img_path, img_path)
        
        im = cv2.imread(img_path)
        expected = np.zeros_like(im)
        
        self.assertTrue(np.array_equal(actual, expected), "The images should be identical.")


if __name__ == '__main__':
    unittest.main()