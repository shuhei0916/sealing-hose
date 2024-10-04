import cv2
import numpy as np

def get_video_properties(cap):
    """ビデオファイルからフレームレート、幅、高さを取得する"""
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return fps, frame_width, frame_height


def draw_contours(frame, contours):
    """輪郭に矩形を描画する"""
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 200:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5, cv2.LINE_4)
    return frame


def create_test_video_with_doodles(input_video_path, output_video_path, doodle_probability=0.05):
    # 動画を読み込む
    cap = cv2.VideoCapture(input_video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {input_video_path}")
        return
    
    fps, frame_width, frame_height = get_video_properties(cap)
    
    # 出力動画の設定
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height), isColor=True)
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # ランダムな確率で落書きを挿入
        if np.random.rand() < doodle_probability:
            # 落書き：ランダムな位置に矩形を描く
            x1, y1 = np.random.randint(0, frame_width//2), np.random.randint(0, frame_height//2)
            x2, y2 = np.random.randint(frame_width//2, frame_width), np.random.randint(frame_height//2, frame_height)
            color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))  # ランダムな色
            thickness = np.random.randint(2, 6)  # ランダムな厚さ
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
        
        # フレームを書き込む
        out.write(frame)
        cv2.imshow('Difference between Videos', frame)
                
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    print(f"Video with doodles saved to {output_video_path}")

def main():
    input_video_path = 'data/vtest.avi'  # 既存の動画ファイルパス
    output_video_path = 'data/dst/vtest_with_doodles.mp4'  # 出力先の動画ファイルパス
    create_test_video_with_doodles(input_video_path, output_video_path)
    
if __name__ == '__main__':
    main()
