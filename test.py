from color_extract import hsv_mask
from common import get_config, getexepath, confirm_consistency
import os
import cv2
import time
import numpy as np
import shutil
from MCTest import writeData


# 
def get_video_info(video_path):
    cap = cv2.VideoCapture(video_path)

    video_info = {}
    video_info["fps"] = cap.get(cv2.CAP_PROP_FPS)
    video_info["frame_width"] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_info["frame_height"] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_info["filename"] = os.path.basename(video_path)

    return video_info

# これなに！？！？！
def extract_color_mask(frame, target_hsv):
    mask = hsv_mask(frame, target_hsv)
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    mu = cv2.moments(gray, False)
    if mu["m00"] != 0:
        x = int(mu["m10"] / mu["m00"])
        y = int(mu["m01"] / mu["m00"])
    else:
        x, y = None, None

    return mask, x, y

def is_match(x, y, current_mask):
    if x is None or y is None:
        return False

    return tuple(current_mask[y, x]) != (0, 0, 0)


def main():
    if not confirm_consistency():
        return 0
        
    settings = get_config()

    target_color = [44, 154, 84]
    test_video = './test_data/raw_videos/01.mp4'
    video_info = get_video_info(test_video)

    output_dir = os.path.join(settings["exe_path"], "master_data", "color_extracted")
    shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    cap = cv2.VideoCapture(test_video)

    # 書き出し用のVideoWriterの設定
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(os.path.join(output_dir, "output.mp4"), fourcc, video_info["fps"], (video_info["frame_width"], video_info["frame_height"]))

    frame_count = 0
    anomaly_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        filename = 'master' + str(frame_count + int(settings["track_length"] / 2)) + '.npy'
        master_track_frame = np.load(os.path.join(settings["exe_path"], "master_data", "color_extracted", filename))

        test_frame, x, y = extract_color_mask(frame, target_color)

        # 重心位置に x印を書く
        cv2.line(test_frame, (x-5,y-5), (x+5,y+5), (0, 0, 255), 2)
        cv2.line(test_frame, (x+5,y-5), (x-5,y+5), (0, 0, 255), 2)

        # このフレームの状態
        is_frame_matched = is_match(x, y, master_track_frame)
        if not is_frame_matched:
            anomaly_count += 1 # 異常度をインクリメント
            if anomaly_count <= settings["anomaly_threshold_frames"]:
                print("anomaly detected!!")

                # 要チェック！
                sendMC = "02FF00044D20000000C8010010"
                writeData(sendMC)

        cv2.putText(test_frame, str(is_frame_matched), (x-15, y-30), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(169, 195, 247), thickness=1)

        # 重心の座標を書き込む
        cv2.putText(test_frame, str((x, y)), (x-15, y-15), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(169, 195, 247), thickness=1)

        # masterの軌跡フレームとテストフレームを足し合わせる
        combined_frame = cv2.add(master_track_frame, test_frame)

        cv2.imshow('combined_frame', combined_frame)

        out.write(combined_frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break

        frame_count += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


# """
# テストモードの実行ファイル    
# 元動画からマーカー抽出→異常判定→通知

# 重心計算やパスの取得など、testとmasterどちらにも共通する処理は別のファイルに書いて参照するようにする。
# 優先度は高くないが、15フレームぶんtestの動画が再生されない問題を解決する。

# 処理の順番がめちゃくちゃなので整理
# """

# from color_extract import hsv_mask
# import sys
# import os
# import cv2
# import time
# import numpy as np
# import shutil
# from MCTest import writeData

# def main():
#     # Parameters for lucas kanade optical flow
#     lk_params = dict( winSize  = (15,15),
#                     maxLevel = 2,
#                     criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))


#     # テキストファイルから取得するなど、コードを参照しなくても変更可能なようにする予定
#     target_color = [44, 154, 84]
#     track_len = 30 
#     track_thickness = 10
#     anomaly_threshold = 100 # 異常が何フレーム連続したら通知を出すのかのしきい値
    
    
#     exe_path = getexepath()
#     test_vid = os.path.join(exe_path, 'test_data', 'raw_videos', '02.mp4') # どれを入力とするのかを決める部分を実装する
#     output_dir = os.path.join(exe_path, 'master_data', 'color_extracted')
    
#     print("exe_path: " + exe_path)
#     print("test_vid: " + test_vid)
#     print("output_dir: " + output_dir)

#     # color_extractedを空にする
#     # shutil.rmtree(output_dir)
#     # os.mkdir(output_dir)
    
    
#     cap = cv2.VideoCapture(test_vid)

#     # 入力動画からフレームレートとフレームサイズを取得
#     fps = 30 #cap.get(cv2.CAP_PROP_FPS)
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     # VideoWriterオブジェクトを作成
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v'はMP4形式のコーデック
#     out = cv2.VideoWriter('./data/0318_0102.mp4', fourcc, fps, (frame_width, frame_height))

#     counter = 0
#     anomaly_level = 0
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # counterぎれの場合の処理を書く（masterとtestでフレームの長さが違う場合）
#         # half_track_lenはもっといい書き方がある気がします。
#         filename = 'master' + str(counter + int(track_len / 2)) + '.npy'
        
#         # ファイルが見つからない時の処理をここに追加予定
#         if not filename: 
#             break
        
#         name = os.path.join(exe_path, 'master_data', 'color_extracted', filename)
#         master_track_frame = np.load(name)
        
#         # cv2.imshow('HSV Mask', master_track_frame)
                
#         test_frame = hsv_mask(frame, target_color)
#         test_frame_gray = cv2.cvtColor(test_frame, cv2.COLOR_BGR2GRAY)
        
#         # シンプルな重心計算
#         mu = cv2.moments(test_frame_gray, False)
#         if mu["m00"] != 0:
#             x,y = int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
#         else:
#             print("No object found")  # 追跡対象が見つからない場合の処理

#         # 重心位置に x印を書く
#         cv2.line(test_frame, (x-5,y-5), (x+5,y+5), (0, 0, 255), 2)
#         cv2.line(test_frame, (x+5,y-5), (x-5,y+5), (0, 0, 255), 2)
                
#         # このフレームの状態
#         st = is_match(x, y, master_track_frame)
#         if not st:
#             anomaly_level += 1 # 異常度をインクリメント
#             if anomaly_level <= anomaly_threshold:
#                 print("anomaly detected!!")
                
#                 # 要チェック！
#                 sendMC = "02FF00044D20000000C8010010"
#                 writeData(sendMC) # 
                
                
#         cv2.putText(test_frame, str(st), (x-15, y-30), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(169, 195, 247), thickness=1)
        
        
#         # 重心の座標を書き込む
#         cv2.putText(test_frame, str((x, y)), (x-15, y-15), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(169, 195, 247), thickness=1)
        
        
#         # masterの軌跡フレームとテストフレームを足し合わせる（addweightedの方が良いかも）
#         combined_frame = cv2.add(master_track_frame, test_frame)
        
#         cv2.imshow('combined_frame', combined_frame)


#         out.write(combined_frame)
        
#         if cv2.waitKey(5) & 0xFF == 27:
#             break

#         counter += 1
        
#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()
    
# def getexepath():
#     if getattr(sys, 'frozen', False):
#         # 実行ファイルからの実行時
#         print("running from exe file...")
#         my_path = os.path.dirname(os.path.abspath(sys.argv[0]))
#         print("my_path:" + my_path)
#         exe_path = my_path + '/../' # 環境によっては別の参照方法の方が良い可能性あり。
#         exe_path = os.path.normpath(exe_path)
#     else:
#         # スクリプトからの実行時
#         print("running from script...")
#         exe_path = os.getcwd()
#         # print('getcwd:      ', os.getcwd())
#         # print('__file__:    ', __file__)
#     return exe_path

# # 引数の座標が軌跡上にあるかどうか
# def is_match(x, y, current_mask):
#     return tuple(current_mask[y, x]) != (0, 0, 0)


# if __name__ == "__main__":
#     main()