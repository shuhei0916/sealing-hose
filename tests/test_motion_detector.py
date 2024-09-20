import unittest
from unittest.mock import Mock
import numpy as np
import cv2
from src import motion_detector as md

class TestAbsDiff(unittest.TestCase):
    def setUp(self):
        self.img1 = cv2.imread('data/lena.jpg')
        self.img2 = cv2.imread('data/lena_q25.jpg')
        self.assertIsNotNone(self.img1, 'Failed to load image from "data/lena.jpg"')
        self.assertIsNotNone(self.img2, 'Failed to load image from "data/lena_q25.jpg"')
        
    def test_identical_images(self):
        actual = cv2.absdiff(self.img1, self.img1)
        expected = np.zeros_like(self.img1)
        self.assertTrue(np.array_equal(actual, expected), 'Expected the identical images to have no differences.')
            
    def test_different_images(self):
        img_diff = cv2.absdiff(self.img1, self.img2)
        self.assertTrue(np.any(img_diff > 0), 'Expected the two images to have pixel differences.')


class TestMotionDetector(unittest.TestCase):
    def test_get_video_properties(self):
        cap = Mock()
        cap.get.side_effect = [30.0, 1920, 1080]

        fps, frame_width, frame_height = md.get_video_properties(cap)

        self.assertEqual(fps, 30.0)
        self.assertEqual(frame_width, 1920)
        self.assertEqual(frame_height, 1080)

        
if __name__ == '__main__':
    unittest.main()