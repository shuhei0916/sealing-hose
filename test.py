"""
テストモードの実行ファイル    
元動画からマーカー抽出→異常判定→通知

重心計算やパスの取得など、testとmasterどちらにも共通する処理は別のファイルに書いて参照するようにする。
優先度は高くないが、15フレームぶんtestの動画が再生されない問題を解決する。

処理の順番がめちゃくちゃなので整理
"""

from color_extract import hsv_mask
import sys
import os
import cv2
import time
import numpy as np
import shutil

def main():
    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                    maxLevel = 2,
                    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))


    # テキストファイルから取得するなど、コードを参照しなくても変更可能なようにする予定
    target_color = [44, 154, 84]
    track_len = 30 
    track_thickness = 10
    
    
    exe_path = getexepath()
    input_vid = os.path.join(exe_path, 'master_data', 'raw_video', '01.mp4')
    output_dir = os.path.join(exe_path, 'master_data', 'color_extracted')
    
    print("exe_path: " + exe_path)
    print("input_vid: " + input_vid)
    print("output_dir: " + output_dir)

    # color_extractedを空にする
    # shutil.rmtree(output_dir)
    # os.mkdir(output_dir)
    
    
    cap = cv2.VideoCapture(input_vid)

    # # 入力動画からフレームレートとフレームサイズを取得
    # fps = 30 #cap.get(cv2.CAP_PROP_FPS)
    # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # # VideoWriterオブジェクトを作成
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v'はMP4形式のコーデック
    # out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    counter = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # counterぎれの場合の処理を書く（masterとtestでフレームの長さが違う場合）
        # half_track_lenはもっといい書き方がある気がします。
        filename = 'master' + str(counter + int(track_len / 2)) + '.npy'
        
        # ファイルが見つからない時の処理をここに追加予定
        if not filename: 
            break
        
        name = os.path.join(exe_path, 'master_data', 'color_extracted', filename)
        master_track_frame = np.load(name)
        
        # cv2.imshow('HSV Mask', master_track_frame)
                
        test_frame = hsv_mask(frame, target_color)
        test_frame_gray = cv2.cvtColor(test_frame, cv2.COLOR_BGR2GRAY)
        
        # シンプルな重心計算
        mu = cv2.moments(test_frame_gray, False)
        if mu["m00"] != 0:
            x,y = int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
        else:
            print("No object found")  # 追跡対象が見つからない場合の処理

        # 重心位置に x印を書く
        cv2.line(test_frame, (x-5,y-5), (x+5,y+5), (0, 0, 255), 2)
        cv2.line(test_frame, (x+5,y-5), (x-5,y+5), (0, 0, 255), 2)
                
        
        # print(is_match(x, y, master_track_frame))
        
        cv2.putText(test_frame, str(is_match(x, y, master_track_frame)), (x-15, y-30), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(169, 195, 247), thickness=1)
        
        # 重心の座標を書き込む
        cv2.putText(test_frame, str((x, y)), (x-15, y-15), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(169, 195, 247), thickness=1)
        
        
        # masterの軌跡フレームとテストフレームを足し合わせる（addweightedの方が良いかも）
        combined_frame = cv2.add(master_track_frame, test_frame)
        
        cv2.imshow('combined_frame', combined_frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break

        counter += 1
        
    cap.release()
    # out.release()
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
        # print('getcwd:      ', os.getcwd())
        # print('__file__:    ', __file__)
    return exe_path

# 引数の座標が軌跡上にあるかどうか
def is_match(a, b, current_mask):
    x = int(a)
    y = int(b)
    return tuple(current_mask[x, y]) != (0, 0, 0)


if __name__ == "__main__":
    main()