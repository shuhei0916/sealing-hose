"""masterやtestに共通の処理をまとめた。"""

import sys
import os

# 設定ファイルの読み込み
def get_config():
    with open("setting.txt", "r") as f:
        lines = f.readlines()

    settings = {}
    for line in lines:
        key, value = line.strip().split("=")
        settings[key] = value

    return settings


def getexepath():
    if getattr(sys, 'frozen', False):
        # 実行ファイルからの実行時
        print("running from exe file...")
        my_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        print("my_path:" + my_path)
        exe_path = my_path + '/../' # 環境によっては別の方法の方が良い可能性あり。
        exe_path = os.path.normpath(exe_path)
    else:
        # スクリプトからの実行時
        print("running from script...")
        exe_path = os.getcwd()
    return exe_path
    