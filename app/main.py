from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from app.image_processor import make_seamless_image
import uuid

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse("app/static/index.html")

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    input_path = f"temp/{uuid.uuid4()}_input.png"
    output_path = f"temp/{uuid.uuid4()}_output.png"

    os.makedirs("temp", exist_ok=True)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    make_seamless_image(input_path, output_path)

    return FileResponse(output_path, media_type="image/png", filename="seamless_output.png")
