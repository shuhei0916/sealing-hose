#####---------- 通信モジュール ----------#####
import socket           #通信用モジュール

#####---------- 通信設定 ----------#####
HOST = '192.168.250.1'  #通信相手機器のIPアドレス設定
PORT = 1100             #使用ポートの設定

#####---------- MCプロトコル　コマンド説明 （例）----------#####
mc_comand = '01FF00044420000005360800'                      #Dデバイスの1334から1341までの8点分を一括で読出す 1sでタイムアウト

"""

    01          #一括読出し
    FF          #固定
    0004        #待ち時間*250ms
    4420        #データレジスタ(D***)
    00000536    #デバイス番号   1334
    08          #点数              8
    00          #終了コード

"""

#####---------- 通信の流れ ----------#####
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #通信用オブジェクトの取得
client.connect((HOST, PORT))                                #クライアント接続

client.send(mc_comand.encode("ascii"))                      #コマンドの送信 → ASCIIコード変換

response = client.recv(2048)                                #応答用のメモリを確保し、取得
client.close()                                              #クライアント接続終了

com_test = response[2:4]                                    #1行の数列でデータが返信される為、必要に応じて分解
com_test = com_test.decode('utf-8')                         #使用可能なコードに変換
print(com_test)                                             #返信の確認

#####---------- MCプロトコル　コマンド説明 ----------#####

"""
    #以下ASCIIコードでのコマンド例

    #サブヘッダ → 書込み、読出し方法の設定
    00  #bit単位での読出し
    01  #word単位での読出し
    02  #bit単位での書込み
    03  #word単位での書込み

    #PC番号
    FF  #固定

    #監視タイマ
    0000    #無限待ち
    0001    #指定数*250ms監視
    
    #デバイス
    ※基本DかMのどちらかで良いと思います
    4420    #D word
    5220    #R word
    4D20    #M bit
    5320    #S bit

    #アドレス
    00000000    #アドレス番号を16進数に変換する
    10  → 0000000A
    100 → 00000064

    #デバイス点数
    01  #読出し、書込みするデバイス点数を16進数に変換

    #終了コード
    00  #固定

"""

######---------- MCプロトコル　送信 ----------#####
sendMC = "02FF00044D2000000064010010"       #シーリングホース異常時
sendMC = "02FF00044D2000000064010000"       #シーリングホース正常時

"""
    02          :bitデバイス一括書込み
    FF          :固定
    0004        :1s監視
    4D20        :補助リレー(M)
    00000064    :100
    01          :1点
    00          :終了コード
    1           :書込みデータ
    0           :ダミーデータ（書込み点数が奇数の場合のみ）
"""

def writeData(sendMC:str) -> tuple[str, str]:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #通信用オブジェクトの取得
    client.connect((HOST, PORT))                                #クライアント接続

    client.send(sendMC.encode("ascii"))                         #コマンドの送信 → ASCIIコード変換

    response = client.recv(256)                                 #応答用のメモリを確保し、取得
    client.close()                                              #クライアント接続終了

    respData = response.decode('utf-8')                         #使用可能なコードに変換
    print(respData)                                             #返信の確認

    comStatus = respData[2:4]                                   #終了コード取出し
    Code = response[4:6]

    return comStatus, Code                                      #異常コード

######---------- MCプロトコル　受信 ----------#####
sendMC = "00FF00044D20000000640400" #送信文

"""
    00          :bitデバイス一括読出し
    FF          :固定
    0004        :1s監視
    4D20        :補助リレー(M)
    00000064    :100
    04          :4点
    00          :終了コード
"""

def readData(sendMC:str) -> tuple[str, str]:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #通信用オブジェクトの取得
    client.connect((HOST, PORT))                                #クライアント接続

    client.send(sendMC.encode("ascii"))                         #コマンドの送信 → ASCIIコード変換

    response = client.recv(256)                                 #応答用のメモリを確保し、取得
    client.close()                                              #クライアント接続終了

    respData = response.decode('utf-8')                         #使用可能なコードに変換
    print(respData)                                             #返信の確認
    comStatus = respData[2:4]                                   #終了コード取出し

    if comStatus == "00":                                       #正常終了であれば
        rbStatus = respData[4:5]                                #ロボットの状態取得
        productCode = respData[5:8]  
        productCode.reverse()                           
        productNumber = str(int(productCode, 2))      #品番取得

    elif comStatus == "5B":                                     #異常終了であれば
        anomalousCode = response[4:6]
        
        return comStatus, anomalousCode                         #異常コード
    
    return rbStatus, productNumber