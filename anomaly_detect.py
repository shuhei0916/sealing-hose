"""
マスターの軌跡フレームを読み込み、フレームを足し合わせ、
テスト動画の座標が足し合わせたフレームの白い部分にあるかどうかを検証する

テスト動画の座標とマスターのフレームを足し合わせながら描画する
is_match関数の定義

"""

import cv2
import numpy as np
import os
from sklearn.cluster import DBSCAN

# マスターの軌跡フレームが保存されているディレクトリ名
dir = "./data/mask_frames" # "./master_video/track_frames"
vid_name = "GX01"

# ファイル名の処理（どのふぃあるを選択するのか）は今後要改良
test_vid = "./test_videos/color_extracted/GX01_masked.mp4"
NUM_FRAMES_TO_COMBINE = 10

WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
PINK = (255, 0, 255)

# params for ShiTomasi corner detection
# blockSizeについては要調査
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 0.1,
                       blockSize = 7)


# クラスタリング用関数
def dbscan_cluster(p0):
    # p0を適切な形に変換
    p0 = np.float32(p0).reshape(-1, 2)
    # DBSCANクラスタリング
    dbscan = DBSCAN(eps=50, min_samples=2)
    labels = dbscan.fit_predict(p0)

    # クラスタリング結果を取得
    unique_labels = set(labels)

    alist = []
    for k in unique_labels:
        # print(k)
        # ノイズの処理
        if k == -1:
            continue

        # k番目のクラスタに属する点の集合
        class_member_mask = (labels == k)

        # クラスタの点
        xy = p0[class_member_mask]
        # ここで各クラスタに対して何かをする（例：重心計算）
        centroid = np.mean(xy, axis=0)
        # print("Cluster: ", k, " Centroid: ", centroid,"pointnum : ", len(xy))
        alist.append(centroid)
    alist = np.array(alist)
    #print(f"p0: {p0}, alist: {alist}")
    p0 = alist.reshape(-1,1, 2)
    return p0


# 定義したよ～～（2024/02/19）
def is_match(a, b, current_mask):
    x = int(a)
    y = int(b)
    return tuple(current_mask[x, y]) != BLACK


def add_frames(start, end):
    # masterの初期化
    master_frame = None
    for i in range(start, end):
        frame_filename = dir + "/" + vid_name + "_" + str(i) + ".jpg"
        # print(frame_filename)/
        
        # 指定されたファイル名の画像を読み込む
        frame = cv2.imread(frame_filename)
        if frame is None:
            print(" skipped!")
            continue # 画像が存在しない場合はスキップ
        
        # combined_frameがまだ初期化されていない場合、現在のフレームと同じサイズで初期化
        if master_frame is None:
            master_frame = np.zeros_like(frame, dtype=np.float64)
        
        # 画像を足し合わせる
        master_frame += frame
    
    # 足し合わせた値をクリップしてuint8に変換
    master_frame = np.clip(master_frame, 0, 255).astype(np.uint8)
    
    # combined_frame = cv2.add(combined_frame, test_frame)
    return master_frame


def main():
    # dir直下のファイル数num_frames
    num_frames = sum(1 for entry in os.scandir(dir) if entry.is_file())
    # print(num_frames)
    
    test_cap = cv2.VideoCapture(test_vid)
    # 最初のフレームの処理
    ret, old_frame = test_cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    # Take first frame and find corners in it
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    #多数検出した特徴点をクラスタリングして、各クラスタ内の平均座標を返す
    p0 = dbscan_cluster(p0)
    
    # 各種プロパティーを取得
    frame_width = int(test_cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # フレームの幅
    frame_height = int(test_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # フレームの高さ
    fps = float(test_cap.get(cv2.CAP_PROP_FPS))  # FPS
    
    # VideoWriter を作成する。
    output_file = "./data/output_video.mp4"  # 保存する動画ファイル名
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 動画のコーデックを指定
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    frame_count = 0
    while True:
        # print("frame_count:", frame_count)

        
        # 現在のフレーム番号から前後NUM_FRAMES_TO_COMBINEフレームの範囲を計算
        start_frame = clamp(frame_count - NUM_FRAMES_TO_COMBINE, 0, num_frames)
        end_frame = clamp(frame_count + NUM_FRAMES_TO_COMBINE + 1, 0, num_frames)
        
        master_frame = add_frames(start_frame, end_frame)
        
        
        
        # テスト動画のしょり
        ret, test_frame = test_cap.read()
        if test_frame is None:
            break
        
        frame_gray = cv2.cvtColor(test_frame, cv2.COLOR_BGR2GRAY)

        # Initialize a mask for the res
        res = np.zeros_like(test_frame)
        
        p0 = cv2.goodFeaturesToTrack(frame_gray, mask = None, **feature_params)
        #多数検出した特徴点をクラスタリングして、各クラスタ内の平均座標を返す
        p0 = dbscan_cluster(p0)
        
        for point in p0:
            # print(point)
            x, y = point.ravel()
            res = cv2.circle(res,(int(x),int(y)),5, PINK, -1)
            # is_match(x, y, )kokokoko
        
        # combined_frame = cv2.add(res, master_frame)
        combined_frame = cv2.addWeighted(master_frame, 0.3, res, 0.7, 0.0)
        
        # 表示
        cv2.imshow("combined frame", combined_frame)
        out.write(combined_frame)
        
        ch = cv2.waitKey(1)
        if ch == 27:
            break
        
        frame_count += 1
    
    test_cap.release()
    out.release()

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

if __name__ == "__main__":
    main()