import cv2
import mediapipe as mp

# MediaPipeの設定
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 動画のキャプチャ
cap = cv2.VideoCapture('vtest.avi')  # your_video.mp4 を再生したい動画のパスに変更

# Poseのインスタンスを作成
with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("ビデオの読み込みが終了しました。")
            break

        # フレームの色をBGRからRGBに変換
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # 骨格検出の実行
        results = pose.process(image)

        # フレームを再度書き込み可能にする
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 検出した骨格を描画
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # 結果の表示
        cv2.imshow('MediaPipe Pose', image)

        # キー入力で終了
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# リソースを解放
cap.release()
cv2.destroyAllWindows()
