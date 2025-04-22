from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import io
from image_processor import swap_left_right, make_tile_seamless, crop_center_square

app = FastAPI()

# フロントエンドの静的ファイル
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("app/static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/process_image/")
async def process_image(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    image = crop_center_square(image)
    image = swap_left_right(image)
    image = make_tile_seamless(image)

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
