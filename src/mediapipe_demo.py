import cv2
import mediapipe as mp

# MediaPipeの設定
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Webカメラから入力
cap = cv2.VideoCapture('data/vtest.avi')  # 0はデフォルトのWebカメラを指定

# Poseのインスタンスを作成
with mp_pose.Pose(
    min_detection_confidence=0.5,  # 検出信頼度の閾値
    min_tracking_confidence=0.5    # トラッキング信頼度の閾値
) as pose:
    while cap.isOpened():
        success, image = cap.read()  # Webカメラからフレームを読み込み
        if not success:
            print("Ignoring empty camera frame.")  # フレームが取得できなかった場合の処理
            continue

        # 画像を処理用に書き込み不可に設定
        image.flags.writeable = False
        # フレームの色空間をBGRからRGBに変換（MediaPipeはRGBを使用）
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 骨格検出を実行
        results = pose.process(image)

        # 画像を再び書き込み可能に設定
        image.flags.writeable = True
        # フレームをRGBからBGRに戻す（OpenCVはBGRを使用）
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 検出された骨格をカメラ画像に描画
        mp_drawing.draw_landmarks(
            image,                     # 画像
            results.pose_landmarks,     # 検出された骨格のランドマーク
            mp_pose.POSE_CONNECTIONS,   # 骨格の接続情報
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()  # 描画スタイル
        )

        # 画像を左右反転させて表示（自然な鏡像表示にするため）
        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

        # ESCキーが押されたらループを終了
        if cv2.waitKey(5) & 0xFF == 27:
            break

# リソースを解放
cap.release()
cv2.destroyAllWindows()
