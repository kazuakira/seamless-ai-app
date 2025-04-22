import cv2
import numpy as np

def make_seamless_image(input_path: str, output_path: str):
    img = cv2.imread(input_path)
    height, width = img.shape[:2]

    # 正方形にトリミング
    size = min(height, width)
    cropped = img[0:size, 0:size]

    # シームレス化（単純なタイル接続模倣: 左右・上下をブレンド）
    half = size // 2
    left = cropped[:, :half]
    right = cropped[:, half:]
    blended = cv2.addWeighted(left, 0.5, right, 0.5, 0)

    result = np.hstack([blended, blended])
    result = np.vstack([result, result])

    cv2.imwrite(output_path, result)
