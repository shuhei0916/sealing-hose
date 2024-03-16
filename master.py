"""
MASTERモードの実行ファイル    
元動画からマーカー抽出→軌跡のフレームを保存

pathの指定方法のエラーに対する対策
    os.path.joinを用いる。
    パスの結合は実行ファイルから実行時の親ファイル参照時に使ってます。
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
    track_len = 50 
    track_thickness = 50
    
    
    exe_path = getexepath()
    input_vid = os.path.join(exe_path, 'master_data', 'raw_video', '01.mp4')
    output_dir = os.path.join(exe_path, 'master_data', 'color_extracted')
    
    print("exe_path: " + exe_path)
    print("input_vid: " + input_vid)
    print("output_dir: " + output_dir)

    # color_extractedを空にする
    shutil.rmtree(output_dir)
    os.mkdir(output_dir)
    
    
    cap = cv2.VideoCapture(input_vid)

    # # 入力動画からフレームレートとフレームサイズを取得
    # fps = 30 #cap.get(cv2.CAP_PROP_FPS)
    # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # # VideoWriterオブジェクトを作成
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v'はMP4形式のコーデック
    # out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

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
        if len(tracks) > track_len:
            tracks.pop(0)
        
        # track_lenの長さだけ軌跡を描画するよう変更予定
        for i in range(1, len(tracks)):
            if tracks[i - 1] is None or tracks[i] is None:
                continue
            cv2.line(res, tracks[i - 1], tracks[i], (255, 255, 0), track_thickness) # resに書き込むのではなく、新しい画像に軌跡のみを描画するように変更予定

        # 重心位置に x印を書く
        # cv2.line(res, (x-5,y-5), (x+5,y+5), (0, 0, 255), 2)
        # cv2.line(res, (x+5,y-5), (x-5,y+5), (0, 0, 255), 2)
        
        
        # 重心の座標を書き込む
        # cv2.putText(res, str((x, y)), (x-15, y-15), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(169, 195, 247), thickness=1)
        
        # 処理されたフレームを出力動画に書き込む（テスト環境用）
        # out.write(res)
        
        # ndarrayの形で保存
        outname = os.path.join(output_dir, 'master' + str(counter))
        np.save(outname, res)
        
        # cv2.imshow('Frame', frame)
        cv2.imshow('HSV Mask', res)

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
    

if __name__ == "__main__":
    main()