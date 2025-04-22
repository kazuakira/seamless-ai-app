from PIL import Image, ImageFilter
import cv2
import numpy as np

def crop_center_square(image: Image.Image) -> Image.Image:
    width, height = image.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    return image.crop((left, top, left + min_dim, top + min_dim))

def swap_left_right(image: Image.Image) -> Image.Image:
    width, height = image.size
    left = image.crop((0, 0, width // 2, height))
    right = image.crop((width // 2, 0, width, height))
    new_image = Image.new('RGB', (width, height))
    new_image.paste(right, (0, 0))
    new_image.paste(left, (width // 2, 0))
    return new_image

def make_tile_seamless(image: Image.Image) -> Image.Image:
    img = np.array(image)
    # ミラーリングで上下左右のつながりを滑らかにする
    top_bottom = cv2.vconcat([img[::-1,:,:], img, img[::-1,:,:]])
    seamless = cv2.GaussianBlur(top_bottom, (0, 0), sigmaX=8)
    mid_h = seamless.shape[0] // 3
    img_blend = seamless[mid_h:mid_h + img.shape[0], :, :]

    left_right = cv2.hconcat([img_blend[:, ::-1, :], img_blend, img_blend[:, ::-1, :]])
    seamless2 = cv2.GaussianBlur(left_right, (0, 0), sigmaX=8)
    mid_w = seamless2.shape[1] // 3
    final = seamless2[:, mid_w:mid_w + img.shape[1], :]

    return Image.fromarray(final)
