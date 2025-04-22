from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline
import torch

# Stable Diffusion パイプラインの初期化（初回はモデルのDLが必要）
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16
).to("cuda")  # CPUのみ環境では .to("cpu") に変更

def crop_to_square(image: Image.Image) -> Image.Image:
    width, height = image.size
    min_edge = min(width, height)
    left = (width - min_edge) // 2
    top = (height - min_edge) // 2
    return image.crop((left, top, left + min_edge, top + min_edge))

def process_image(image: Image.Image) -> Image.Image:
    image = crop_to_square(image)
    image = image.resize((512, 512))
    prompt = "a seamless tileable pattern"
    result = pipe(prompt=prompt, image=image, strength=0.75, guidance_scale=7.5).images[0]
    return result