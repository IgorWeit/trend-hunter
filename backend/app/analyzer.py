import os
import google.generativeai as genai
import requests
import time

def get_youtube_data(query):
    api_key = os.environ.get("YOUTUBE_API_KEY")
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': query,
        'maxResults': 10,
        'type': 'video',
        'order': 'relevance', # Можно заменить на 'viewCount' для поиска самых хайповых
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        items = response.json().get('items', [])
        
        videos = []
        for item in items:
            video_id = item['id']['videoId']
            videos.append({
                'title': item['snippet']['title'],
                'link': f"https://www.youtube.com/watch?v={video_id}",
                'description': item['snippet']['description']
            })
        return videos
    except Exception as e:
        print(f"❌ YouTube API Error: {e}")
        return []

def analyze_trend(data):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key: 
        return "ОШИБКА: API ключ Gemini не найден."
    
    # 1. Получаем реальные данные через API
    real_videos = get_youtube_data(data)
    
    if not real_videos:
        return "⚠️ Не удалось получить данные из YouTube API. Проверьте ключ или лимиты."

    # Подготовка данных для промпта
    video_context = ""
    links_list = ""
    for i, v in enumerate(real_videos, 1):
        video_context += f"{i}. {v['title']}\nОписание: {v['description']}\n\n"
        links_list += f"- {v['link']}\n"

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name='models/gemini-flash-latest')
        
        prompt = f"""
Ты — аналитическая станция The Weit. 
Проведи бизнес-анализ тренда "{data}" на основе следующих реальных данных из YouTube:

ДАННЫЕ ДЛЯ АНАЛИЗА:
{video_context}

ВЫДАЙ ОТЧЕТ СТРОГО ПО ФОРМАТУ:

| Показатель | Значение |
| :--- | :--- |
| Viral Score | [0-10] |
| Товарная ниша | [Название] |
| Средняя вовлеченность | [0.0]% |
| Постов проанализировано | 10 |

### 🎬 УСПЕШНЫЕ РОЛИКИ ХАРАКТЕРИЗУЮТСЯ:
**Сюжет:** [Детальный разбор структуры контента]
**Смысловая нагрузка:** [Ключевые идеи и месседжи]
**Драматургия:** [Как удерживается внимание, какие крючки используются]
**Длительность:** [Средняя оптимальная длина]
**Видеоряд:** [Стилистика, монтаж, визуальные приемы]
**Озвучка:** [Тон, музыкальное сопровождение, подача]
**Другие особенности:** [Уникальные фишки из описаний]
**Ключевой фактор успеха:** [Что именно сделало эти ролики популярными]

**Вывод:** [Итоговая бизнес-рекомендация]

---APPLIED_MATERIAL---
### 📂 ПРИКЛАДНОЙ МАТЕРИАЛ:
Вот ссылки на видео, проанализированные через YouTube Data API v3:
{links_list}
"""
        
        response = model.generate_content(prompt)
        return response.text
            
    except Exception as e:
        return f"❌ Ошибка ИИ-анализа: {str(e)}"