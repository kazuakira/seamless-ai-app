import cv2
import numpy as np
from PIL import Image
import io

def make_seamless_image(image_bytes: bytes) -> bytes:
    # PIL で画像読み込み
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # 正方形にトリミング
    size = min(image.size)
    left = (image.width - size) // 2
    top = (image.height - size) // 2
    image = image.crop((left, top, left + size, top + size))

    # OpenCV に変換
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 上下左右に反転拡張
    bordered = cv2.copyMakeBorder(
        img_cv, size, size, size, size, borderType=cv2.BORDER_REFLECT
    )

    # 中央を切り抜いて戻す
    h, w = img_cv.shape[:2]
    center = bordered[h//2 : h//2 + h, w//2 : w//2 + w]

    # PIL に戻して保存
    result_img = Image.fromarray(cv2.cvtColor(center, cv2.COLOR_BGR2RGB))
    output = io.BytesIO()
    result_img.save(output, format='PNG')
    return output.getvalue()
