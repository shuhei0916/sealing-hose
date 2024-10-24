"""
2024展示会用のデモプログラム。
左画面に動体検知、右画面に骨格検知を行います。
"""

import cv2
import mediapipe as mp
import numpy as np

# MediaPipeの設定
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 動体検知に必要な関数
def get_video_properties(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return fps, frame_width, frame_height

def detect_motion(frame1_gray, frame2_gray):
    motion_diff = cv2.absdiff(frame1_gray, frame2_gray)
    _, thresh = cv2.threshold(motion_diff, 90, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilated = cv2.dilate(thresh, kernel, iterations=2)
    return motion_diff

# Webカメラから入力
cap = cv2.VideoCapture(0)
fps, frame_width, frame_height = get_video_properties(cap)

# 初期フレームの設定
ret, prev_frame = cap.read()
if not ret:
    print("Error: Could not read video frame.")
    cap.release()
    cv2.destroyAllWindows()

frame1_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Poseのインスタンスを作成
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:
    while cap.isOpened():
        ret, current_frame = cap.read()
        if not ret:
            break

        # 骨格検知処理用のフレーム（左半分に表示）
        image_rgb = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        # 検出された骨格を描画
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image_bgr,  # 左半分に表示される骨格検知
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )

        # 動体検知処理用のフレーム（右半分に表示）
        frame2_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        motion_frame = detect_motion(frame1_gray, frame2_gray)

        # 次のループのためにフレームを更新
        frame1_gray = frame2_gray

        # 画像を左右に並べて表示するための準備
        motion_frame_colored = cv2.cvtColor(motion_frame, cv2.COLOR_GRAY2BGR)

        # 左半分：骨格検知結果、右半分：動体検知結果
        combined_frame = np.hstack((image_bgr, motion_frame_colored))

        # 画像を表示（左右反転も適用）
        cv2.imshow('Pose (Left) & Motion Detection (Right)', cv2.flip(combined_frame, 1))

        # ESCキーが押されたらループを終了
        if cv2.waitKey(5) & 0xFF == 27:
            break

# リソースを解放
cap.release()
cv2.destroyAllWindows()
