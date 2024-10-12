import cv2
import numpy as np
from common import get_video_properties, draw_contours

def find_best_matching_frame(frame, master_frames):
    min_diff_sum = float('inf')
    best_frame = None
    
    for master_frame in master_frames:
        master_frame_gray = cv2.cvtColor(master_frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(frame, master_frame_gray)
        diff_sum = np.sum(diff)
        
        if diff_sum < min_diff_sum:
            min_diff_sum = diff_sum
            best_frame = master_frame
    
    return best_frame

def display_video_difference_with_window(video_path1, video_path2, output_path1, output_path2, window_size=30):
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)
    
    if not (cap1.isOpened() and cap2.isOpened()):
        print("Error: Could not open one or both videos.")
        return
    
    fps, frame_width, frame_height = get_video_properties(cap1)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out1 = cv2.VideoWriter(output_path1, fourcc, fps, (frame_width, frame_height), isColor=False)
    out2 = cv2.VideoWriter(output_path2, fourcc, fps, (frame_width, frame_height), isColor=True)

    abnormal_frame_count = 0
    threshold_sum = 1e6
    master_frames = []
    
    while cap1.isOpened() and cap2.isOpened():
        ret1, master_frame = cap1.read()
        ret2, test_frame = cap2.read()
        
        if not (ret1 and ret2):
            break
        
        # マスターデータから前後30フレームを取得
        master_frames.append(master_frame)
        if len(master_frames) > window_size * 2:
            master_frames.pop(0)

        test_frame_gray = cv2.cvtColor(test_frame, cv2.COLOR_BGR2GRAY)
        
        if len(master_frames) >= window_size * 2:
            best_master_frame = find_best_matching_frame(test_frame_gray, master_frames)
            
            best_master_frame_gray = cv2.cvtColor(best_master_frame, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(test_frame_gray, best_master_frame_gray)
            
            diff_sum = np.sum(diff)
            if diff_sum > threshold_sum:
                abnormal_frame_count += 1

            _, thresh = cv2.threshold(diff, 90, 255, cv2.THRESH_BINARY)
            
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            dilated = cv2.dilate(thresh, kernel, iterations=2)
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            frame_with_contours = draw_contours(test_frame.copy(), contours)
            
            out1.write(diff)
            cv2.imshow('Difference between Videos', diff)
            
            # out2.write(frame_with_contours)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()
    
    print(f"Total abnormal frames detected: {abnormal_frame_count}")
    
    
if __name__ == '__main__': 
    master_video_path = 'data/gr1_crop1m.mp4'
    test_video_path = 'data/gr1_crop2m.mp4'
    diff_output_path = 'data/dst/gr1_diff_with_frames.mp4'
    contour_output_path = 'data/dst/gr1_diff_with_frames_contours.mp4'
    
    
    # 二つの動画の差分を表示
    display_video_difference_with_window(master_video_path, test_video_path, diff_output_path, contour_output_path)

