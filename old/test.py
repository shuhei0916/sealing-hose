"""
テストモードの実行ファイル    
元動画からマーカー抽出→異常判定→通知

重心計算やパスの取得など、testとmasterどちらにも共通する処理は別のファイルに書いて参照するようにする。
優先度は高くないが、15フレームぶんtestの動画が再生されない問題を解決する。

"""

from color_extract import hsv_mask
from common import get_config, getexepath
import sys
import os
import cv2
import time
import numpy as np
import shutil
from MCTest import writeData
import datetime
from video_cap import vid_cap


def main():
    # カレントディレクトリの取得
    exe_path = getexepath()
    
    while True:

        # 録画したデータを保存するディレクトリを指定
        input_dir = os.path.join(exe_path, 'test_data', 'raw_videos')

        # 録画の開始
        dt_now = datetime.datetime.now()
        vid_name = dt_now.strftime('%m%d_%H%M')
        vid_cap(input_dir, vid_name)

        # 録画終了後、計算処理開始
        # input_dir直下にあるファイルのうち一つだけが選択される
        input_file = os.listdir(input_dir)[0] 
        input_vid = os.path.join(input_dir, input_file)

        # input_vid = os.path.join(exe_path, 'data', '03.mp4') # 簡易デバッグ用
        anomaly_detect(input_vid, exe_path)

        if cv2.waitKey(1) & 0xFF == 27:
            break


    # # output_dirを空にする
    # shutil.rmtree(output_dir)
    # os.mkdir(output_dir)


def anomaly_detect(test_vid, exe_path):

    target_color = [31, 127, 37] # green

    # 設定ファイルの読み込み
    settings = get_config()

    cap = cv2.VideoCapture(test_vid)

    # 入力動画からフレームレートとフレームサイズを取得
    fps = 30 #cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # VideoWriterオブジェクトを作成
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v'はMP4形式のコーデック
    out = cv2.VideoWriter('./data/0328test3.mp4', fourcc, fps, (frame_width, frame_height))

    counter = 0
    anomaly_level = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # counterぎれの場合の処理を書く（masterとtestでフレームの長さが違う場合）
        filename = 'master' + str(counter + int(int(settings["track_thickness"]) / 2)) + '.npy'
        name = os.path.join(exe_path, 'master_data', 'track_frames', filename)
       
        # ファイルが見つからない時の処理
        try:    
            master_track_frame = np.load(name)
        except FileNotFoundError:
            print("file not found!")
            break


        # cv2.imshow('HSV Mask', master_track_frame)
                
        test_frame = hsv_mask(frame, target_color)
        test_frame_gray = cv2.cvtColor(test_frame, cv2.COLOR_BGR2GRAY)
        
        # シンプルな重心計算
        mu = cv2.moments(test_frame_gray, False)
        if mu["m00"] != 0:
            x,y = int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
            # このフレームの状態
            st = is_match(x, y, master_track_frame)
        else:
            # print("No object found")  # 追跡対象が見つからない場合の処理
            pass
    

        if not st:
            anomaly_level += 1      

        # masterの軌跡フレームとテストフレームを足し合わせる（addweightedの方が良いかも）
        combined_frame = cv2.add(master_track_frame, frame)

        # 重心位置に x印を書く
        cv2.line(combined_frame, (x-5,y-5), (x+5,y+5), (0, 0, 255), 2)
        cv2.line(combined_frame, (x+5,y-5), (x-5,y+5), (0, 0, 255), 2)

        # 異常のStatusを書き込む
        cv2.putText(combined_frame, str(st), (x-15, y-30), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0, 0, 255), thickness=1)
        
        # 重心の座標を書き込む
        cv2.putText(combined_frame, str((x, y)), (x-15, y-15), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0, 0, 255), thickness=1)
                
        cv2.imshow('anomly_detect', combined_frame)

        out.write(combined_frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

        counter += 1
    

    # この後、anomaly_levelによって分岐処理
    print("anomaly_level:", anomaly_level)
    if anomaly_level > int(settings["anomaly_threshold"]):
        print("anomaly detected!")

        sendMC = "02FF00044D20000000C8010010"
        writeData(sendMC)
        # キー入力待ち
        while True:
            if cv2.waitKey(1) & 0xFF == ord("r"):
                # 異常ランプをOFFにする
                sendMC = "02FF00044D20000000C8010000" 
                writeData(sendMC)
                break

    else:
        print("no anomaly detected!")

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    

def getexepath():
    if getattr(sys, 'frozen', False):
        # 実行ファイルからの実行時
        print("running from exe file...")
        my_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        print("my_path:" + my_path)
        exe_path = my_path + '/../' # 環境によっては別の参照方法の方が良い可能性あり。
        exe_path = os.path.normpath(exe_path)
    else:
        # スクリプトからの実行時
        print("running from script...")
        exe_path = os.getcwd()
    return exe_path


# 引数の座標が軌跡上にあるかどうか
def is_match(x, y, current_mask):
    return tuple(current_mask[y, x]) != (0, 0, 0)


if __name__ == "__main__":
    main()






# # 
# def extract_color_mask(frame, target_hsv):
#     mask = hsv_mask(frame, target_hsv)
#     gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

#     mu = cv2.moments(gray, False)
#     if mu["m00"] != 0:
#         x = int(mu["m10"] / mu["m00"])
#         y = int(mu["m01"] / mu["m00"])
#     else:
#         x, y = None, None

#     return mask, x, y

# def is_match(x, y, current_mask):
#     if x is None or y is None:
#         return False

#     return tuple(current_mask[y, x]) != (0, 0, 0)


# def main():
#     if not confirm_consistency():
#         return 0
        
#     # 設定ファイルの読み込み
#     settings = get_config()

#     # カレントディレクトリの取得
#     exe_path = getexepath()

#     target_color = [44, 154, 84]

#     test_video = os.path.join('./test_data', 'raw_videos', '01.mp4') 
#     output_dir = os.path.join(exe_path, "master_data", "anomaly_detect") 

#     # output_dirを空にする
#     shutil.rmtree(output_dir)
#     os.mkdir(output_dir)

#     cap = cv2.VideoCapture(test_video)

#     # 入力動画の情報を取得
#     fps = 30 # cap.get(cv2.CAP_PROP_FPS)
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     # 書き出し用のVideoWriterの設定
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(os.path.join(output_dir, "output.mp4"), fourcc, fps, (frame_width, frame_height))

#     frame_count = 0
#     anomaly_count = 0

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         filename = 'master' + str(frame_count + int(settings["track_length"] / 2)) + '.npy'
#         master_track_frame = np.load(os.path.join(exe_path, "master_data", "track_frames", filename))

#         test_frame, x, y = extract_color_mask(frame, target_color)

#         # 重心位置に x印を書く
#         cv2.line(test_frame, (x-5,y-5), (x+5,y+5), (0, 0, 255), 2)
#         cv2.line(test_frame, (x+5,y-5), (x-5,y+5), (0, 0, 255), 2)

#         # このフレームの状態
#         is_frame_matched = is_match(x, y, master_track_frame)
#         if not is_frame_matched:
#             anomaly_count += 1 # 異常度をインクリメント
#             if anomaly_count <= settings["anomaly_threshold"]:
#                 print("anomaly detected!!")

#                 # 要チェック！
#                 sendMC = "02FF00044D20000000C8010010"
#                 writeData(sendMC)

#         cv2.putText(test_frame, str(is_frame_matched), (x-15, y-30), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(169, 195, 247), thickness=1)

#         # 重心の座標を書き込む
#         cv2.putText(test_frame, str((x, y)), (x-15, y-15), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(169, 195, 247), thickness=1)

#         # masterの軌跡フレームとテストフレームを足し合わせる
#         combined_frame = cv2.add(master_track_frame, test_frame)

#         cv2.imshow('combined_frame', combined_frame)

#         out.write(combined_frame)

#         if cv2.waitKey(5) & 0xFF == 27:
#             break

#         frame_count += 1

#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()


