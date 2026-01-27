from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List # <-- Для списков
import uvicorn

from .analyzer import analyze_trend
from .scraper import get_real_trends
from .trends_service import get_trends_data # <-- НОВЫЙ ИМПОРТ

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель для одного слова (для анализа)
class TrendRequest(BaseModel):
    category: str

# НОВАЯ Модель для сравнения (принимает список слов)
class CompareRequest(BaseModel):
    keywords: List[str]

@app.get("/")
def read_root():
    return {"status": "TrendHunter AI is active"}

# --- СТАРЫЙ МАРШРУТ (Анализ стратегии) ---
@app.post("/analyze")
def start_analysis(request: TrendRequest):
    print(f"🔎 Анализ стратегии: {request.category}")
    try:
        real_data = get_real_trends(request.category)
        analysis_result = analyze_trend(real_data)
        return {"status": "success", "analysis": analysis_result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- НОВЫЙ МАРШРУТ (Графики) ---
@app.post("/compare")
def compare_trends(request: CompareRequest):
    print(f"📊 Сравнение: {request.keywords}")
    try:
        # Вызываем функцию из trends_service.py
        data = get_trends_data(request.keywords)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)