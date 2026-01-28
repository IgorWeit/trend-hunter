from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.analyzer import analyze_trend
import os

app = FastAPI()

# Подключаем статику
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

class AnalyzeRequest(BaseModel):
    url: str

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    result = analyze_trend(request.url)
    return {"result": result}

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")
