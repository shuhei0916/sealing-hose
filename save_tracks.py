'''
正常時の動画を入力として、その軌跡を描画・保存するスクリプト。
track.pyより分割（2024/01/09）
'''

import numpy as np
import cv2
import os
from sklearn.cluster import DBSCAN
import shutil

WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
PINK = (255, 0, 255)

# anomaly_detectで選択できるようにした方がよいか。要検討
THICKNESS = 20

# params for ShiTomasi corner detection
# blockSizeについては要調査
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 0.1,
                       blockSize = 7)

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

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

def main():
    dirname = "./master_video/color_extracted/"
    video_name = "GX01" # 正常時の動画を選択
    input_path = dirname + video_name + "_masked.mp4"
    output_path = "./master_video/track_frames" 

    # output_pathを初期化
    shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)
    
    print(f"Input Path: {input_path}")
    print(f"Output Path: {output_path}")

    cap = cv2.VideoCapture(input_path)
    
    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    # Take first frame and find corners in it
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

    # print(len(p0))
    # print(f"p0 before reshape:{p0}")
    
    #多数検出した特徴点をクラスタリングして、各クラスタ内の平均座標を返す
    p0 = dbscan_cluster(p0)
    
    all_masks = [] # 各フレームの軌跡
    line_retain_frames = 1 #軌跡の残留フレーム

    frame_counter = 0
    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Initialize a mask for the current frame
        current_mask = np.zeros_like(frame)
        
        # 遮蔽されたときの処理
        if len(p0) <= 1:
            pn = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
            pn = dbscan_cluster(pn)
            # 遮蔽から戻るときの処理
            if len(pn) > len(p0):
                p0 = pn
            
        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        
        # Select good points
        try:
            good_new = p1[st==1]
            good_old = p0[st==1]
            # print("good_new: "+ str(good_new))
            # print("good_old: "+ str(good_old))
        except:
            print("st is None", p0)
            continue

        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            current_mask = cv2.line(current_mask, (int(a),int(b)),(int(c),int(d)), WHITE, thickness=THICKNESS)
            # frame = cv2.circle(frame,(int(a),int(b)),5, WHITE, -1)
        
        # 
        all_masks.append(current_mask)
        combined_mask = np.zeros_like(frame)

        # 今のフレームからline_retain_frames遡ったフレームまでの軌跡を足す
        for mask in all_masks[-line_retain_frames:]: 
            combined_mask = cv2.add(combined_mask, mask)
        img = cv2.add(frame,combined_mask)
        
        # img = cv2.add(frame, current_mask)

        # この時点で、combined_maskには白い軌跡とカラフルな軌跡を合わせたもの、
        # current_maskにはカラフルな軌跡のみ（今は一時停止中）
        # imgには元のフレームに軌跡を合成したものが入っている
        
        # マスクを保存
        cv2.imwrite(output_path + "/" + video_name + "_" + str(frame_counter) + ".jpg", combined_mask)
       
        # 描画
        cv2.imshow('frame', combined_mask)
        
        # writer.write(img)
        
        k = cv2.waitKey(30) & 0xff
        if k == 27: # ESCで終了
            break
        
        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1,1,2)
        
        #フレームのカウンタを更新
        frame_counter += 1
        
        
    # 終了処理
    cv2.destroyAllWindows()
    cap.release()
    # writer.release()
    
    combined_mask_all = np.zeros_like(frame)
    for mask in all_masks:
        combined_mask_all = cv2.add(combined_mask, mask)

    # np.save(dirname + '/mask_checkpoint/'+ video_name +'_mask_all', combined_mask)
    print("Done!")
       

if __name__ == '__main__':
    main()