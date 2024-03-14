"""
テストモードの実行ファイル    
元動画からマーカー抽出→異常判定→通知
"""

from color_extract import hsv_mask
import sys
import os
import cv2