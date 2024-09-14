import cv2
import numpy as np

def calc_diff(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    im_diff = img1.astype(int) - img2.astype(int)
    im_diff_abs = np.abs(im_diff)
    print(f'{im_diff_abs=}')
    
    return im_diff_abs


def main():
    im= cv2.imread('data/saizeriya1.jpg')
    print(im.shape)
    print(im.dtype)

if __name__ == '__main__':
    main()