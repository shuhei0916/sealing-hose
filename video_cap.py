"""
録画を行うコード    
"""

import cv2
import os
from MCTest import writeData, readData

def vid_cap(save_directory):

    # 保存先ディレクトリが存在しない場合は作成
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # カメラの初期化
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("カメラが開けません")
        exit()
        
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # 動画ファイルの保存設定
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_path = os.path.join(save_directory, "output.mp4")
    out = cv2.VideoWriter(out_path, fourcc, 30.0, (640, 480))
    
    recording = False  # 録画開始フラグ

    print("Press 's' to start/stop recording. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()

        # PCLとの通信部分
        sendMC = "00FF00044D20000000640800" 
        rbStatus, productNo = readData(sendMC) 

        if not ret:
            print("Failed to grab frame")
            break

        # フレームの表示
        cv2.imshow("title", frame)

        key = cv2.waitKey(1) & 0xFF
        if rbStatus == "1":   # if key == ord('s'):
            
            # いったんOFFにする
            sendMC = "02FF00044D20000000C8010000" 
            writeData(sendMC)

            print("productNo:", productNo)
            recording = not recording  # 録画の開始/停止をトグル
            if recording:
                print("Recording started...")
            else:
                print("Recording stopped.")
        
        # 録画中の場合、フレームを書き込む
        if recording:
            out.write(frame)

        if key == ord("q"):
            break

    # リソースの解放
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def main():
    print("hehe")


if __name__ == "__main__":
    main()
