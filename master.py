"""
masterのTODO:
    vid_cap部分をmaster.py内に含める

"""

from color_extract import hsv_mask
from common import get_config, getexepath, get_config
from video_cap import vid_cap
import os
import cv2
import time
import numpy as np
import shutil
import datetime


def main():

    target_color = [44, 154, 84] # green
    
    # 設定ファイルの読み込み
    settings = get_config()

    # カレントディレクトリの取得
    exe_path = getexepath()

    input_dir = os.path.join(exe_path, 'master_data', 'raw_video')

    # 録画の開始
    dt_now = datetime.datetime.now()
    vid_name = dt_now.strftime('%m%d_%H%M')
    vid_cap(input_dir, vid_name)

    input_file = os.listdir(input_dir)[0] # input_dir直下にあるファイルのうち一つだけが選択される

    input_vid = os.path.join(input_dir, input_file)
    output_dir = os.path.join(exe_path, 'master_data', 'track_frames')
    
    print("exe_path: " + exe_path)
    print("input_vid: " + input_vid)
    print("output_dir: " + output_dir)

    print("track_length: ", settings["track_length"])
    print("track_thickness: ", settings["track_thickness"])
    print("anomaly_threshold: ", settings["anomaly_threshold"])

    # exit(0)

    # out_directoryを空にする
    shutil.rmtree(output_dir)
    os.mkdir(output_dir)
    
    
    cap = cv2.VideoCapture(input_vid)

    tracks = []
    counter = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        res = hsv_mask(frame, target_color)
        
        res_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        
        # シンプルな重心計算
        mu = cv2.moments(res_gray, False)
        if mu["m00"] != 0:
            x,y = int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
            # 軌跡を保存するためのコードをここに追加
        else:
            print("No object found")  # 追跡対象が見つからない場合の処理
            # 必要に応じて、追跡対象が見つからない状態を処理するコードをここに追加
        tracks.append((x, y))
        # tracksの長さがtrack_lenより大きい場合、最も古い要素を削除
        if len(tracks) > int(settings["track_length"]):
            tracks.pop(0)
        
        # track_lenの長さだけ軌跡を描画するよう変更予定
        for i in range(1, len(tracks)):
            if tracks[i - 1] is None or tracks[i] is None:
                continue
            cv2.line(res, tracks[i - 1], tracks[i], (255, 255, 0), int(settings["track_thickness"])) # resに書き込むのではなく、新しい画像に軌跡のみを描画するように変更予定

        
        # ndarrayの形で保存
        outname = os.path.join(output_dir, 'master' + str(counter))
        np.save(outname, res)
        
        # cv2.imshow('Frame', frame)
        cv2.imshow('HSV Mask', res)

        if cv2.waitKey(5) & 0xFF == 27:
            break

        counter += 1
        
    cap.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    main()