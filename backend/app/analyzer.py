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
        'order': 'relevance',
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
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name='models/gemini-flash-latest')

        # ШАГ 1: Исследование (Google Research через ИИ)
        research_prompt = f"На основе запроса '{data}' сформируй лучший поисковый запрос для YouTube, чтобы найти самые успешные и виральные ролики в этой нише. Выдай только текст запроса."
        search_query_response = model.generate_content(research_prompt)
        search_query = search_query_response.text.strip() if search_query_response.text else data
        
        # ШАГ 2: Сбор данных с YouTube
        real_videos = get_youtube_data(search_query)
        if not real_videos:
            return "⚠️ YouTube API не вернул данных. Проверьте лимиты ключа."

        video_context = ""
        links_list = ""
        for i, v in enumerate(real_videos, 1):
            video_context += f"Видео {i}: {v['title']}\nОписание: {v['description']}\n\n"
            links_list += f"{v['link']}\n"

        # ШАГ 3: Глубокий анализ по твоей структуре
        final_prompt = f"""
Ты — аналитическая станция The Weit. 
Проведи глубокий разбор тренда на основе этих 10 реальных роликов из YouTube:

{video_context}

ВЫДАЙ ОТЧЕТ СТРОГО ПО ЭТОМУ ФОРМАТУ:

### 🎬 УСПЕШНЫЕ РОЛИКИ ХАРАКТЕРИЗУЮТСЯ:
**Сюжет:** [Разбор структуры]
**Смысловая нагрузка:** [О чем контент]
**Драматургия:** [Как держат внимание]
**Длительность:** [Оптимальный тайминг]
**Видеоряд:** [Визуал и монтаж]
**Озвучка:** [Звук и подача]
**Другие особенности:** [Фишки]
**Ключевой фактор успеха:** [Почему это смотрят]

**Вывод:** [Бизнес-совет]

---APPLIED_MATERIAL---
### 📂 ПРИКЛАДНОЙ МАТЕРИАЛ:
Ссылки на проанализированные видео:
{links_list}
"""
        
        response = model.generate_content(final_prompt)
        return response.text
            
    except Exception as e:
        return f"❌ Ошибка системы: {str(e)}"