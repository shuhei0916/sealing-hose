import cv2
from common import process_frame

def display_video_difference(video_path1, video_path2):
    """2つのビデオの差分を計算して表示"""
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)
    
    if not (cap1.isOpened() and cap2.isOpened()):
        print("Error: Could not open one or both videos.")
        return
    
    while cap1.isOpened() and cap2.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        
        if not (ret1 and ret2):
            break
        
        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # 2つのフレームの差分を計算
        diff = process_frame(frame1_gray, frame2_gray)
        
        # 結果を表示
        cv2.imshow('Difference between Videos', diff)
        
        # 'q'キーで終了
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_path1 = 'data/gr2_crop1.mp4'
    video_path2 = 'data/gr2_crop2.mp4'
    
    # 二つの動画の差分を表示
    display_video_difference(video_path1, video_path2)
