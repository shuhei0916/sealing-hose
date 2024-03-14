import time
from datetime import datetime
import os
import sys
from hehe import my_add


print(my_add(2, 4))
time.sleep(5)

# path = os.getcwd()
# print(path)

# print("hehe")
# # exe_path = os.path.dirname(os.path.abspath(sys.argv[0]))
# # print("exe_path: " + exe_path)
# # script_dir = sys._MEIPASS

# # print("script_dir:" + script_dir)

# if getattr(sys, 'frozen', False):
#     # 実行ファイルからの実行時
#     my_path = os.path.dirname(os.path.abspath(sys.argv[0]))
#     exe_path = my_path + '/../'
#     exe_path = os.path.normpath(exe_path)
# else:
#     # スクリプトからの実行時
#     exe_path = os.getcwd()
#     # print('getcwd:      ', os.getcwd())
#     # print('__file__:    ', __file__)
    
# print('exe_path:' + exe_path)
# # file_path = os.path.join(script_dir, "sample.csv")


# time.sleep(10)