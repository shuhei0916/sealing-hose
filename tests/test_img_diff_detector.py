import unittest
import numpy as np
import cv2
import src.img_diff_detector as dd

class TestImgDiffDetector(unittest.TestCase):
    def setUp(self):
        self.img1 = cv2.imread('data/lena.jpg')
        self.img2 = cv2.imread('data/lena_q25.jpg')
        self.assertIsNotNone(self.img1, "Failed to load image from 'data/lena.jpg'")
        self.assertIsNotNone(self.img2, "Failed to load image from 'data/lena_q25.jpg'")
        
    def test_identical_images(self):
        actual = cv2.absdiff(self.img1, self.img1)
        expected = np.zeros_like(self.img1)
        self.assertTrue(np.array_equal(actual, expected), 'Expected the identical images to have no differences.')
            
    def test_different_images(self):
        img_diff = cv2.absdiff(self.img1, self.img2)
        self.assertTrue(np.any(img_diff > 0), 'Expected the two images to have pixel differences.')


if __name__ == '__main__':
    unittest.main()