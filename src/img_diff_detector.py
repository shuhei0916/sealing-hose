import cv2
import numpy as np

def calc_diff(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    im_diff = img1.astype(int) - img2.astype(int)
    im_diff_abs = np.abs(im_diff)
    
    return im_diff_abs


def main():
    im1 = cv2.imread('data/lena.jpg')
    im2 = cv2.imread('data/lena_q25.jpg')
    
    im_diff = calc_diff('data/lena.jpg', 'data/lena_q25.jpg')
    cv2.imwrite('data/dst/lena_diff.jpg', im_diff)
    

if __name__ == '__main__':
    main()