import cv2
import numpy as np
from common import get_video_properties, draw_contours, find_contours

# NOTE: master->reference, test->targetのように改名したほうが良いかも
def display_video_difference(master_video_path, test_video_path, diff_output_path, contour_output_path, window_size=30):
    cap1 = cv2.VideoCapture(master_video_path)
    cap2 = cv2.VideoCapture(test_video_path)
    
    if not (cap1.isOpened() and cap2.isOpened()):
        print("Error: Could not open one or both videos.")
        return
    
    fps, frame_width, frame_height = get_video_properties(cap1)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    diff_video_writer = cv2.VideoWriter(diff_output_path, fourcc, fps, (frame_width, frame_height), isColor=False)
    contour_video_writer = cv2.VideoWriter(contour_output_path, fourcc, fps, (frame_width, frame_height), isColor=True)

    abnormal_frame_count = 0
    threshold_sum = 1e6
    
    while cap1.isOpened() and cap2.isOpened():
        ret1, master_frame = cap1.read()
        ret2, test_frame = cap2.read()
        
        if not (ret1 and ret2):
            break
                
        master_frame_gray = cv2.cvtColor(master_frame, cv2.COLOR_BGR2GRAY)
        test_frame_gray = cv2.cvtColor(test_frame, cv2.COLOR_BGR2GRAY)
                
        # フレームのサイズが一致しているか確認 NOTE: 不要かも？
        if master_frame_gray.shape != test_frame_gray.shape:
            test_frame_gray = cv2.resize(test_frame_gray, (master_frame_gray.shape[1], master_frame_gray.shape[0]))

        diff = cv2.absdiff(master_frame_gray, test_frame_gray)
        
        diff_sum = np.sum(diff)

        if diff_sum > threshold_sum:
            abnormal_frame_count += 1
        
        
                
        copy = test_frame.copy()
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 200:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(copy, (x, y), (x + w, y + h), (0, 255, 0), 5, cv2.LINE_4)
                
           
        # frame_with_contours = draw_contours(test_frame.copy(), contours)
        
        
        # TOOD: このロジックに対する自動テスト書く
        # diff_ratio = np.sum(dilated) / (frame_width * frame_height)
        # if diff_ratio > 1500: # NOTE: この閾値は今後調整する
        #     print('Anomaly detected!')

        
        cv2.imshow('Difference between Videos', copy)
        
        # diff_video_writer.write(diff)
        # contour_video_writer.write(frame_with_contours)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
        
    # print(diff )
    # print(diff.shape)
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()
    
    print(f"Total abnormal frames detected: {abnormal_frame_count}")


if __name__ == '__main__': 
    master_video_path = 'data/vtest.avi'
    test_video_path = 'data/dst/vtest_with_doodles.mp4'
    diff_output_path = 'data/dst/vtest_diff.mp4'
    contour_output_path = 'data/dst/vtest_diff_contours.mp4'
    
    
    # 二つの動画の差分を表示
    display_video_difference(master_video_path, test_video_path, diff_output_path, contour_output_path)
