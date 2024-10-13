'''
https://developers.cyberagent.co.jp/blog/archives/12666/
これを参考に動体検知を作り直したもの
'''

import cv2
import numpy as np
from common import draw_contours, draw_contours_with_rectangle

def main():
    video_path = 'data/vtest.avi'
    output_path = 'data/dst/vtest_processed.mp4'

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    fps, frame_width, frame_height = int(cap.get(cv2.CAP_PROP_FPS)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), isColor=True)

    # 背景モデル用の変数
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read video frame.")
        return

    avg_frame = np.float32(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 背景モデルを更新（加重平均を使用）
        cv2.accumulateWeighted(gray_frame, avg_frame, 0.01)
        background = cv2.convertScaleAbs(avg_frame)

        # 背景との差分を計算
        diff = cv2.absdiff(gray_frame, background)

        # 差分画像を二値化
        _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated = cv2.dilate(thresh, kernel, iterations=2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        frame_with_contours = frame.copy()
        
        frame_with_contours = draw_contours(frame_with_contours, contours)
        
        cv2.imshow('Motion Detection', frame_with_contours)
        out.write(frame_with_contours)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
