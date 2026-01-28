from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
# Исправленный импорт с учетом вложенности
from backend.app.analyzer import analyze_trend
import os

app = FastAPI()

# Указываем путь к папке static относительно корня проекта
static_path = os.path.join(os.getcwd(), "backend", "static")

@app.post("/analyze")
async def analyze(request: BaseModel):
    url = getattr(request, 'url', None)
    result = analyze_trend(url)
    return {"result": result}

@app.get("/")
async def read_index():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": f"Index file not found at {index_file}. Current dir: {os.getcwd()}"}

if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
