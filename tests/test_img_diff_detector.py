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
        
        self.assertTrue(np.array_equal(actual, expected), 'The images should be identical.')\
            
            
    def test_different_images(self):
        img_path1 = 'data/lena.jpg'
        img_path2 = 'data/lena_q25.jpg'
        actual = dd.calc_diff(img_path1, img_path2)

        self.assertTrue(np.any(actual > 0), 'The images should have differences.')


    def test_calc_diff_matches_absdiff(self):
        img_path1 = 'data/lena.jpg'
        img_path2 = 'data/lena_q25.jpg'
        
        actual = dd.calc_diff(img_path1, img_path2)
        im1 = cv2.imread(img_path1)
        im2 = cv2.imread(img_path2)
        expected = cv2.absdiff(im1, im2)

        self.assertTrue(np.array_equal(actual, expected),  'The calculated image difference does not match the expected result.')



if __name__ == '__main__':
    unittest.main()