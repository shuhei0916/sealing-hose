import cv2

def get_video_properties(cap):
    """ビデオファイルからフレームレート、幅、高さを取得する"""
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return fps, frame_width, frame_height


def draw_contours(frame, contours):
    """輪郭に矩形を描画する"""
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 200:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5, cv2.LINE_4)
    return frame
