import unittest
import src.img_diff_detector as dd

class TestImgDiffDetector(unittest.TestCase):
    def test_identical_images(self):
        img1 = 'data/saizeriya1.jpg'
        # img3 = 'data/saizeriya1.jpg'
        actual = dd.calc_diff(img1, img1)
        expected = 0
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()