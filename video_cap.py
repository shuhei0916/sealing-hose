"""
録画を行うコード
TODO:
    cv2.DSHOWの後処理：上下反転する

"""

import cv2
import os
from MCTest import writeData, readData
import datetime
import shutil


def main():  

    MODE = "MASTER"
    # 現在の日時を取得
    dt_now = datetime.datetime.now()
    print(dt_now.strftime('%m%d_%H%M'))
    vid_name = dt_now.strftime('%m%d_%H%M')

    if MODE == "MASTER":
        save_directory = "./master_data/raw_video" 
    else:
        save_directory = "./test_data/raw_videos"

    print(save_directory)
    vid_cap(save_directory, vid_name)


def vid_cap(save_directory, vid_name):

    # save_directoryを空にする
    shutil.rmtree(save_directory)
    os.mkdir(save_directory)


    # カメラの初期化
    cap = cv2.VideoCapture("./data/01.mp4") # , cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("can't open the camera.")
        exit()

    # fpsを30に固定    
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # 入力動画の情報を取得
    fps = 30 #cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 動画ファイルの保存設定
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    vid_name = vid_name + ".mp4"
    out_path = os.path.join(save_directory, vid_name)
    out = cv2.VideoWriter(out_path, fourcc, fps, (frame_width, frame_height)) 


    recording = False  # 録画開始フラグ

    print("Press 's' to start/stop recording. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()

        # PCLとの通信部分
        # sendMC = "00FF00044D20000000640800" 
        # rbStatus, productNo = readData(sendMC) 

        if not ret:
            print("Failed to grab frame")
            break

        # フレームの表示
        cv2.imshow("title", frame)
        key = cv2.waitKey(1) & 0xFF

        # PLCからの立ち上がり信号があったら、録画開始
        if key == ord('s'): # rbStatus == "1":
            
            # # 異常ランプをOFFにする
            # sendMC = "02FF00044D20000000C8010000" 
            # writeData(sendMC)

            # print("productNo:", productNo)
            recording = not recording  # 録画の開始/停止をトグル
            if recording:
                print("Recording started...")
            else:
                print("Recording stopped.")
                break
        
        # 録画中の場合、フレームを書き込む
        if recording:
            out.write(frame)

        # if key == ord("q"):
        #     break


    # リソースの解放
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("vid_cap finished!")


if __name__ == "__main__":
    main()
