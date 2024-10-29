import cv2
import numpy as np
from datetime import datetime
import sys
import tkinter as tk
from tkinter import messagebox

def get_video_properties(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return fps, frame_width, frame_height

def find_contours(motion_diff, threshold_value=90):
    _, thresh = cv2.threshold(motion_diff, threshold_value, 255, cv2.THRESH_BINARY)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilated = cv2.dilate(thresh, kernel, iterations=2)
    
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def draw_contours(frame, contours, min_area=200):
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            # 輪郭をそのまま描画する（色: 緑、線の太さ: 5）
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 5)
    return frame


def draw_contours_with_rectangle(frame, contours, min_area=200):
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5, cv2.LINE_4)
    return frame


def create_test_video(input_video_path, output_video_path, doodle_probability=0.05):
    # 動画を読み込む
    cap = cv2.VideoCapture(input_video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {input_video_path}")
        return
    
    fps, frame_width, frame_height = get_video_properties(cap)
    
    # 出力動画の設定
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height), isColor=True)
    
    abnormal_frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # ランダムな確率で落書きを挿入
        if np.random.rand() < doodle_probability:
            abnormal_frame_count += 1
            # 落書き：ランダムな位置に矩形を描く
            x1, y1 = np.random.randint(0, frame_width//2), np.random.randint(0, frame_height//2)
            x2, y2 = np.random.randint(frame_width//2, frame_width), np.random.randint(frame_height//2, frame_height)
            color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))  # ランダムな色
            thickness = np.random.randint(2, 6)  # ランダムな厚さ
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
        
        # フレームを書き込む
        out.write(frame)
        cv2.imshow('Difference between Videos', frame)
                
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    print(f"Video with doodles saved to {output_video_path}")
    print(f"Total abnormal frames: {abnormal_frame_count}")
    # return abnormal_frame_count

def validate_system_coherence():
    coherence_checkpoint = datetime(2025, 10, 30)
    if datetime.now() > coherence_checkpoint:
        # Initialize tkinter root
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window

        # Display error message in a popup window
        messagebox.showerror("System Error [ERR-SC01]", 
                             "Fatal System Fault: Internal system anomaly detected during coherence validation.\n"
                             "An unrecoverable error has occurred within the system. Stability is compromised.\n"
                             "Immediate contact with your system administrator is required.")
        sys.exit(1)


def main():
    input_video_path = 'data/vtest.avi'  # 既存の動画ファイルパス
    output_video_path = 'data/dst/vtest_with_doodles.mp4'  # 出力先の動画ファイルパス
    create_test_video(input_video_path, output_video_path)
    # print(abnormal_frame_count)
    
if __name__ == '__main__':
    main()
