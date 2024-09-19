import cv2
import numpy as np


def main():
    im1 = cv2.imread('data/lena.jpg')
    im2 = cv2.imread('data/lena_q25.jpg')
    
    im_diff = cv2.absdiff(im1, im2)
    cv2.imwrite('data/dst/lena_diff.jpg', im_diff)
    

if __name__ == '__main__':
    main()