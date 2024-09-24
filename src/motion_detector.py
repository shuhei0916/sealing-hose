import cv2
import numpy as np
import sys

def get_video_properties(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return fps, frame_width, frame_height


def main():
    video_path = 'data/vtest_10sec.mp4'
    output_path = 'data/dst/thresh_10sec.mp4'
    
    cap = cv2.VideoCapture(video_path)
    
    fps, frame_width, frame_height = get_video_properties(cap)    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), isColor=False)

    ret, frame1 = cap.read()
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    
    while cap.isOpened():
        ret, frame2 = cap.read()
        if not ret:
            break
        
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(frame1_gray, frame2_gray)
        
        
        # 動きのある領域を強調するために閾値処理を適用
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        # 差分を膨張させて小さなノイズを除去（モルフォロジー変換）
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilated = cv2.dilate(thresh, kernel, iterations=2) 
        
        cv2.imshow('Motion Detection', thresh)
        out.write(thresh)
        
        frame1_gray = frame2_gray
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    out.release()
    cv2.destroyWindow('hoge')
        

if __name__ == '__main__':
    main()