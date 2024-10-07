import cv2
import numpy as np
from common import get_video_properties, draw_contours

def display_video_difference(video_path1, video_path2, output_path1, output_path2):
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)
    
    if not (cap1.isOpened() and cap2.isOpened()):
        print("Error: Could not open one or both videos.")
        return
    
    fps, frame_width, frame_height = get_video_properties(cap1)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out1 = cv2.VideoWriter(output_path1, fourcc, fps, (frame_width, frame_height), isColor=False)
    out2 = cv2.VideoWriter(output_path2, fourcc, fps, (frame_width, frame_height), isColor=True)

    
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
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        frame_with_contours = draw_contours(frame2.copy(), contours)
        
        
        # TOOD: このロジックに対する自動テスト書く
        diff_ratio = np.sum(dilated) / (frame_width * frame_height)
        # if diff_ratio > 1500: # NOTE: この閾値は今後調整する
        #     print('Anomaly detected!')

        
        cv2.imshow('Difference between Videos', diff)
        
        out1.write(diff)
        out2.write(frame_with_contours)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
        
    # print(diff )
    # print(diff.shape)
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()


if __name__ == '__main__': 
    video_path1 = 'data/gr1_crop1m.mp4'
    video_path2 = 'data/gr1_crop2m.mp4'
    output_path1 = 'data/dst/gr1_diff.mp4'
    output_path2 = 'data/dst/gr1_diff_contour.mp4'
    
    
    # 二つの動画の差分を表示
    display_video_difference(video_path1, video_path2, output_path1, output_path2)
