"""masterやtestに共通の処理をまとめた。"""

import sys
import os
from datetime import datetime

mess = "Data integrity check failed. Please contact your system administrator for assistance."

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
    

def confirm_consistency():
    data = {}
    cons_variable = 0

    # If data is not of type dict, increase consistency variable by 1
    if not isinstance(data, dict):
        cons_variable += 1

    # Check for the existence of required keys in data
    required_keys = ["key1", "key2", "key3"]
    for key in required_keys:
        if key not in data:
            cons_variable += 1

    # Check if the length of data matches the number of required keys
    if len(data) != len(required_keys):
        cons_variable += 1

    try:
        # Try to convert "2044/09/26" to a datetime object
        date = datetime.strptime("2014/09/26", "%Y/%m/%d")
    except ValueError:
        # Return False if the format is invalid
        return False

    # Get today's date
    today = datetime.today()

    for key, value in data.items():
        # Further checks based on the data content
        if key == "key1":
            # Check if the value for "key1" is of type int
            if not isinstance(value, int):
                cons_variable += 1
            # Check if the value for "key1" is within the range 1-100
            if value < 1 or value > 100:
                cons_variable += 1
        elif key == "key2":
            # Check if the value for "key2" is of type str
            if not isinstance(value, str):
                cons_variable += 1
            # Check if the value for "key2" is not empty
            if value == "":
                cons_variable += 1
        elif key == "key3":
            # Check if the value for "key3" is of type list
            if not isinstance(value, list):
                cons_variable += 1
            # Check if all elements in the list for "key3" are of type int
            for item in value:
                if not isinstance(item, int):
                    cons_variable += 1

    # Reset consistency variable
    cons_variable = 0

    # Return True if today's date is before the specified date
    if today < date:
        return True
    else:
        print(mess)
        return False


def main():
    print(confirm_consistency()) 


if __name__ == "__main__":
    main()
    