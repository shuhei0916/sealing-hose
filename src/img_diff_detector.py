import cv2
import numpy as np


def main():
    video_path = 'data/vtest.avi'
    cap = cv2.VideoCapture(video_path)

    ret, frame1 = cap.read()
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    
    while cap.isOpened():
        ret, frame2 = cap.read()
        if not ret:
            break
        
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(frame1_gray, frame2_gray)
        
        cv2.imshow('Motion Detection', diff)
        
        frame1_gray = frame2_gray
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cv2.destroyWindow('hoge')
        
        
    

if __name__ == '__main__':
    main()