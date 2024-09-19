import cv2
import numpy as np
import sys

def get_video_properties(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return fps, frame_width, frame_height


def main():
    video_path = 'data/vtest.avi'
    output_path = 'data/dst/output_motion_detection.avi'
    
    cap = cv2.VideoCapture(video_path)
    
    fps, frame_width, frame_height = get_video_properties(cap)    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), isColor=False)

    ret, frame1 = cap.read()
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    
    while cap.isOpened():
        ret, frame2 = cap.read()
        if not ret:
            break
        
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(frame1_gray, frame2_gray)
        
        cv2.imshow('Motion Detection', diff)
        out.write(diff)
        
        frame1_gray = frame2_gray
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    out.release()
    cv2.destroyWindow('hoge')
        

if __name__ == '__main__':
    main()