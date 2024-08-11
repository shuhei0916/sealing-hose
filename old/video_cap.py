"""
録画を行うコード

"""

import cv2
import os
from MCTest import writeData, readData
import datetime
import shutil
import time


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
    cap = cv2.VideoCapture(0) # cv2.CAP_DSHOW
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
    rbStatus_old = None

    memory = datetime.datetime.now()

    while True:
        ret, frame = cap.read()

        # 現在時刻とmemoryの差分を取得
        now = datetime.datetime.now()
        p = datetime.timedelta.total_seconds(now - memory)

        if p > 0.04:
            memory = datetime.datetime.now()

            # PCLとの通信部分
            sendMC = "00FF00044D20000000640800" 
            rbStatus, productNo = readData(sendMC) 

        # print("rbStatus:", rbStatus, ", productNo: ", productNo)
        if not ret:
            print("Failed to grab frame")
            break


        # print("recording:", recording, rbStatus_old, rbStatus)
        text = "recording: " + str(recording) + ", rbStatus: " + str(rbStatus) + ", rbStatus_old: " + str(rbStatus_old)
        cv2.putText(frame, text, (10, 10), cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0, 0, 255), thickness=1)
        
        # フレームの表示
        cv2.imshow("vid_cap", frame)
        key = cv2.waitKey(1) & 0xFF

        # 1 -> 0に切り替わったタイミングで録画開始
        if rbStatus_old == "0" and rbStatus == "1" and not recording:# key == ord('s'): # 
            # 異常ランプをOFFにする
            sendMC = "02FF00044D20000000C8010000" 
            writeData(sendMC)

            recording = True
            print("recording started...")

        # 1 -> 0に切り替わったタイミングで録画停止
        elif rbStatus_old == "1" and rbStatus == "0" and recording:
            recording = False
            print("recording stopped...")  
            break 

        # 録画中の場合、フレームを書き込む
        if recording:
            out.write(frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        

        # rbStatusを更新
        rbStatus_old = rbStatus

    # リソースの解放
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("vid_cap finished!")


if __name__ == "__main__":
    main()
