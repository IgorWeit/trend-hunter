from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.app.analyzer import analyze_trend
import os

app = FastAPI()
static_path = os.path.join(os.getcwd(), "backend", "static")

@app.post("/analyze")
async def analyze(request: dict):
    result = analyze_trend(request)
    return {"result": result}

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_path, "index.html"))

app.mount("/static", StaticFiles(directory=static_path), name="static")
