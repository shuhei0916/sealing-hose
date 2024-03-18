#####---------- 通信モジュール ----------#####
import socket           #通信用モジュール
import time

#####---------- 通信設定 ----------#####
HOST = '192.168.1.250'  #通信相手機器のIPアドレス設定
PORT = 1100             #使用ポートの設定

######---------- MCプロトコル　書込み ----------#####
#sendMC = "02FF00044D2000000064010010"   #異常時
#sendMC = "02FF00044D2000000064010000"   #正常時

#"""
#    02          :bitデバイス一括書込み
#    FF          :固定
#    0004        :1s監視
#    4D20        :補助リレー(M)
#    00000064    :100
#    01          :1点
#    00          :終了コード
#    1           :書込みデータ
#    0           :ダミーデータ（書込み点数が奇数の場合のみ）
#"""

def writeData(sendMC:str) -> tuple[str, str]:
    HOST = '192.168.1.250'  #通信相手機器のIPアドレス設定
    PORT = 1100             #使用ポートの設定
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #通信用オブジェクトの取得
    client.connect((HOST, PORT))                               #クライアント接続

    client.send(sendMC.encode("ascii"))                         #コマンドの送信 → ASCIIコード変換

    response = client.recv(256)                                 #応答用のメモリを確保し、取得
    client.close()                                              #クライアント接続終了

    respData = response.decode('utf-8')                         #使用可能なコードに変換
    #print(respData)                                             #返信の確認

    comStatus = respData[2:4]                                   #終了コード取出し
    Code = response[4:6]

    return comStatus, Code                                      #異常コード

######---------- MCプロトコル　受信 ----------#####
#sendMC = "00FF00044D20000000640400" #送信文

#"""
#    00          :bitデバイス一括読出し
#    FF          :固定
#    0004        :1s監視
#    4D20        :補助リレー(M)
#    00000064    :100
#    04          :4点
#    00          :終了コード
#"""

def readData(sendMC:str) -> tuple[str, str]:
    HOST = '192.168.1.250'  #通信相手機器のIPアドレス設定
    PORT = 1100             #使用ポートの設定
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #通信用オブジェクトの取得
    client.connect((HOST, PORT))                                #クライアント接続

    client.send(sendMC.encode("ascii"))                         #コマンドの送信 → ASCIIコード変換

    response = client.recv(256)                                 #応答用のメモリを確保し、取得
    client.close()                                              #クライアント接続終了

    respData = response.decode('utf-8')                         #使用可能なコードに変換
    #print(respData)                                             #返信の確認
    comStatus = respData[2:4]                                   #終了コード取出し

    if comStatus == "00":                                       #正常終了であれば
        rbStatus = respData[11:12]                                #ロボットの状態取得
        productCode = respData[6:7] + respData[5:6] + respData[4:5]

        productNumber = str(int(productCode, 2))                #品番取得
        print(rbStatus)
        print(productNumber)
    elif comStatus == "5B":                                     #異常終了であれば
        anomalousCode = response[4:6]
        
        return comStatus, anomalousCode                         #異常コード
    
    return rbStatus, productNumber

def main():
    res = True
    while(res):

        sendMC = "00FF00044D20000000640800"         #送信文
        rbStatus, productNo = readData(sendMC)      #正常時 ロボット状態モニタ, 品番
                                                    #異常時 通信状態, 異常コード

        sendMC = "02FF00044D20000000C8010010"       #シーリングホース異常時
        sendMC = "02FF00044D20000000C8010000"       #シーリングホース正常時

        time.sleep(0.01)                            #スキャンタイム用待ち時間

        comStatus, code = writeData(sendMC)         #正常時 通信状態, ""
                                                    #異常時 通信状態, 異常コード
        time.sleep(0.01)                            #スキャンタイム用待ち時間

if __name__ == "__main__":
    main()
    

        