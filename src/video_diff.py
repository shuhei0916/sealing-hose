import cv2
import numpy as np
from common import get_video_properties

def display_video_difference(video_path1, video_path2, output_path):
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)
    
    if not (cap1.isOpened() and cap2.isOpened()):
        print("Error: Could not open one or both videos.")
        return
    
    fps, frame_width, frame_height = get_video_properties(cap1)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), isColor=False)

    
    while cap1.isOpened() and cap2.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        
        if not (ret1 and ret2):
            break
        
        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                
        # フレームのサイズが一致しているか確認
        if frame1_gray.shape != frame2_gray.shape:
            frame2_gray = cv2.resize(frame2_gray, (frame1_gray.shape[1], frame1_gray.shape[0]))

        diff = cv2.absdiff(frame1_gray, frame2_gray)
        
        _, thresh = cv2.threshold(diff, 90, 255, cv2.THRESH_BINARY)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated = cv2.dilate(thresh, kernel, iterations=2)
        
        # TOOD: このロジックに対する自動テスト書く
        diff_ratio = np.sum(dilated) / (frame_width * frame_height)
        if diff_ratio > 1500: # NOTE: jこの閾値は今後調整する
            print('Anomaly detected!')
        
        cv2.imshow('Difference between Videos', diff)
        # out.write(diff)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
        
    # print(diff )
    # print(diff.shape)
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()


if __name__ == '__main__': 
    video_path1 = 'data/Megamind.avi'
    video_path2 = 'data/Megamind_bugy.avi'
    output_path = 'data/dst/Megamind_diff.mp4'
    
    # 二つの動画の差分を表示
    display_video_difference(video_path1, video_path2, output_path)
