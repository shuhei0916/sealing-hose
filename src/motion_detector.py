import cv2
import numpy as np


def get_video_properties(cap):
    """ビデオファイルからフレームレート、幅、高さを取得する"""
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return fps, frame_width, frame_height


def process_frame(frame1_gray, frame2_gray):
    """2つのフレームの差分を計算し、閾値処理後に膨張処理を行う"""
    diff = cv2.absdiff(frame1_gray, frame2_gray)
    
    # 閾値処理
    _, thresh = cv2.threshold(diff, 90, 255, cv2.THRESH_BINARY)

    # モルフォロジー変換（膨張）
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilated = cv2.dilate(thresh, kernel, iterations=2)
    
    # return diff
    return dilated


def draw_contours(frame, contours):
    """輪郭に矩形を描画する"""
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 200:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 122, 0), cv2.LINE_4)
    return frame


def main():
    video_path = 'data/Rb.mp4'
    output_path = 'data/dst/Rb_contour.mp4'
    
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
        cv2.imshow('Motion Detection', frame_with_contours)
        out.write(frame_with_contours)

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
