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

def create_test_video(output_path, fps=30, width=640, height=480, duration=5):
    # 動画の作成
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for _ in range(fps * duration):  # フレーム数 = fps * duration
        # 正常なフレームを生成（ランダムな色の背景）
        frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        
        # ある確率で異常なフレームを挿入
        if np.random.rand() > 0.95:
            # 異常なフレーム（黒い矩形を入れる）
            cv2.rectangle(frame, (100, 100), (300, 300), (0, 0, 0), -1)
        
        out.write(frame)
    
    out.release()
    
def main():
    print("hoge")

if __name__ == '__main__':
    main()
