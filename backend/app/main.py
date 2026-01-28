from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.analyzer import analyze_trend
import os

app = FastAPI()

# Определяем абсолютный путь к папке static
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_path = os.path.join(current_dir, "static")

@app.post("/analyze")
async def analyze(request: BaseModel):
    # Универсальный прием данных
    url = getattr(request, 'url', None)
    result = analyze_trend(url)
    return {"result": result}

@app.get("/")
async def read_index():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": f"Index file not found at {index_file}"}

# Монтируем статику в конце
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
