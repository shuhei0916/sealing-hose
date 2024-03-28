import cv2
import os

def video_to_frames(video_path, output_dir):
  """
  動画をフレームに分割して保存します。

  Args:
    video_path: 入力動画ファイルのパス
    output_dir: 出力フレーム画像の保存先ディレクトリ

  Returns:
    None
  """

  # 動画キャプチャオブジェクトを取得
  cap = cv2.VideoCapture(video_path)

  # 動画のフレームレートを取得
  fps = cap.get(cv2.CAP_PROP_FPS)

  # フレーム番号を初期化
  frame_count = 0

  # 動画の最後までループ
  while True:
    # 1フレーム読み込み
    ret, frame = cap.read()

    # 読み込みが失敗したらループを抜ける
    if not ret:
      break

    # フレーム画像を保存
    cv2.imwrite(os.path.join(output_dir, f"frame_{frame_count:05d}.jpg"), frame)

    # フレーム番号をインクリメント
    frame_count += 1

  # 動画キャプチャオブジェクトを解放
  cap.release()

# 使用例
video_path = "./data/03.mp4"
output_dir = "./data/spritedframes"

video_to_frames(video_path, output_dir)
