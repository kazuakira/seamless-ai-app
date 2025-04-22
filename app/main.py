from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import io
from .image_processor import process_image

app = FastAPI()

# 静的ファイル（index.html）を提供
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.post("/process_image/")
async def process_image_endpoint(file: UploadFile = File(...)):
    input_image = Image.open(file.file).convert("RGB")
    output_image = process_image(input_image)

    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return StreamingResponse(img_byte_arr, media_type="image/png")
