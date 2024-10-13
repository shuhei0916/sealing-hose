import cv2
import numpy as np
from common import get_video_properties, draw_contours, find_contours

def detect_motion(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    fps, frame_width, frame_height = get_video_properties(cap)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video_writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), isColor=False)

    ret, prev_frame = cap.read()
    if not ret:
        print("Error: Could not read video frame.")
        return
    frame1_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    while cap.isOpened():
        ret, current_frame = cap.read()
        if not ret:
            break

        frame2_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        
        motion_diff = cv2.absdiff(frame1_gray, frame2_gray)
        
        _, thresh = cv2.threshold(motion_diff, 90, 255, cv2.THRESH_BINARY)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated = cv2.dilate(thresh, kernel, iterations=2)
        
        # motion_contours = find_contours(motion_diff)
        
        # frame_with_contours = draw_contours(current_frame.copy(), motion_contours)
        
        

        
        cv2.imshow('Motion Detection', dilated) 
        # output_video_writer.write(frame_with_contours)

        frame1_gray = frame2_gray
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    output_video_writer.release()
    cv2.destroyAllWindows()


def main():
    video_path = 'data/vtest.avi'
    output_path = 'data/dst/vtest_processed.mp4'
    
    detect_motion(video_path, output_path)

if __name__ == '__main__':
    main()
