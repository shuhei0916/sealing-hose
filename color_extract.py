import cv2
import numpy as np
import colorsys

input_path = "./data/01.mp4"
output = "./data/01_pmasked.mp4"

COLOR_TO_EXTRACT = [44, 154, 84]

# [255, 145, 137] # pink
# [44, 154, 84] # green 
# [239, 249, 101] # yellow

def main():
    cap = cv2.VideoCapture(input_path)

    # 入力動画からフレームレートとフレームサイズを取得
    fps = 30 #cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # VideoWriterオブジェクトを作成
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v'はMP4形式のコーデック
    out = cv2.VideoWriter(output, fourcc, fps, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        res = hsv_mask(frame, COLOR_TO_EXTRACT)

        # 処理されたフレームを出力動画に書き込む
        out.write(res)
        
        # cv2.imshow('Frame', frame)
        cv2.imshow('HSV Mask', res)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def hsv_mask(frame, rgb_color):
    # RGBからHSVへ変換
    hsv_color = cv2.cvtColor(np.uint8([[rgb_color]]), cv2.COLOR_RGB2HSV)[0][0]
    # hsv_color = rgb_color
    
    # HSV色空間における色の範囲を計算(hの範囲は0-179で間違いない？要確認)
    h, s, v = hsv_color
    lower_color = np.array([clamp(h - 3, 0, 179), clamp(s - 100, 0, 255), 50])
    upper_color = np.array([clamp(h + 3, 0, 179), clamp(s + 100, 0, 255), 255])

    # 指定された色の範囲内の部分を抽出
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # モルフォロジカル演算を適用してノイズ除去
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # # ガウシアンフィルタを適用
    # mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    # メディアンブラーを適用
    mask = cv2.medianBlur(mask, 5)
    
    return cv2.bitwise_and(frame, frame, mask=mask)
    # return mask


# 値を範囲内に制限（clamp）する
def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


if __name__ == '__main__':
    main()
