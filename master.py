"""
MASTERモードの実行ファイル    
元動画からマーカー抽出→軌跡のフレームを保存
"""

from color_extract import hsv_mask
import sys
import os
import cv2

def main():
    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                    maxLevel = 2,
                    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    
    input_path = "./data/01.mp4"
    output_path = "./data/01_pmasked.mp4"

    COLOR_TO_EXTRACT = [44, 154, 84]
    
    if getattr(sys, 'frozen', False):
        # 実行ファイルからの実行時
        print("running from exe file...")
        my_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        exe_path = my_path + '/../'
        exe_path = os.path.normpath(exe_path)
    else:
        # スクリプトからの実行時
        print("running from script...")
        exe_path = os.getcwd()
        # print('getcwd:      ', os.getcwd())
        # print('__file__:    ', __file__)
    
    print(exe_path)
    
    cap = cv2.VideoCapture(input_path)

    # 入力動画からフレームレートとフレームサイズを取得
    fps = 30 #cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # VideoWriterオブジェクトを作成
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v'はMP4形式のコーデック
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))


    tracks = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        res = hsv_mask(frame, COLOR_TO_EXTRACT)
        
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
        
        for i in range(1, len(tracks)):
            if tracks[i - 1] is None or tracks[i] is None:
                continue
            cv2.line(res, tracks[i - 1], tracks[i], (255, 255, 0), 10)

        # 重心位置に x印を書く
        cv2.line(res, (x-5,y-5), (x+5,y+5), (0, 0, 255), 2)
        cv2.line(res, (x+5,y-5), (x-5,y+5), (0, 0, 255), 2)
        
        
        # 重心の座標を書き込む
        cv2.putText(res, str((x, y)), (x-15, y-15), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(247, 195, 169), thickness=1)
        # 処理されたフレームを出力動画に書き込む
        out.write(res)
        
        # cv2.imshow('Frame', frame)
        cv2.imshow('HSV Mask', res)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()