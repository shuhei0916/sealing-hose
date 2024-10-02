import cv2
import numpy as np
from common import get_video_properties, process_frame, draw_contours


def main():
    video_path = 'data/Rb.mp4'
    output_path = 'data/dst/Rb.mp4'
    
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
        
        # 差分処理と膨張処理を行う
        dilated = process_frame(frame1_gray, frame2_gray)
        
        # 輪郭を抽出
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # フレームに輪郭を描画
        frame_with_contours = draw_contours(frame2.copy(), contours)
        
        # 結果を表示し、保存する
        # cv2.imshow('Motion Detection', frame_with_contours)
        out.write(frame2)

        # 次のフレームを処理するために更新
        frame1_gray = frame2_gray
        
        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 後処理
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
