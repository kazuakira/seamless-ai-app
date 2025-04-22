from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from .image_processor import make_seamless_image
import io

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("app/static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = make_seamless_image(image_bytes)
    return StreamingResponse(io.BytesIO(result), media_type="image/png")
