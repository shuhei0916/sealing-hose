import cv2
import numpy as np
from common import get_video_properties, process_frame, draw_contours


def main():
    video_path = 'data/vtest.avi'
    output_path = 'data/dst/vtest_processed.mp4'
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    # ビデオのプロパティを取得
    fps, frame_width, frame_height = get_video_properties(cap)
    
    # 出力先の設定（グレースケールで保存）
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), isColor=True)

    # 最初のフレームを取得
    ret, frame1 = cap.read()
    if not ret:
        print("Error: Could not read video frame.")
        return
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    while cap.isOpened():
        ret, frame2 = cap.read()
        if not ret:
            break

        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # dilated = process_frame(frame1_gray, frame2_gray)
        diff = cv2.absdiff(frame1_gray, frame2_gray)
        
        _, thresh = cv2.threshold(diff, 90, 255, cv2.THRESH_BINARY)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated = cv2.dilate(thresh, kernel, iterations=2)
        
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        frame_with_contours = draw_contours(frame2.copy(), contours)
        
        cv2.imshow('Motion Detection', diff)
        # out.write(frame2)

        frame1_gray = frame2_gray
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 後処理
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
