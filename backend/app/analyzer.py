import os
import google.generativeai as genai
import requests
import time

def get_youtube_data(query):
    """Получает 10 реальных видео через официальный YouTube Data API v3"""
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
    """Основная логика: Google Research -> YouTube API -> Deep AI Analysis"""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key: 
        return "ОШИБКА: API ключ Gemini не найден."
    
    try:
        # Настройка ИИ (используем самую стабильную модель по нашим тестам)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name='models/gemini-flash-latest')

        # ШАГ 1: Уточнение запроса (Google Research)
        research_prompt = f"Сформируй идеальный поисковый запрос для YouTube, чтобы найти самые виральные видео по теме: '{data}'. Выдай только текст запроса."
        search_query_res = model.generate_content(research_prompt)
        search_query = search_query_res.text.strip() if search_query_res.text else data
        
        # ШАГ 2: Поиск реальных данных
        real_videos = get_youtube_data(search_query)
        if not real_videos:
            return "⚠️ Не удалось найти видео для анализа. Проверьте настройки YouTube API."

        video_context = ""
        links_list = ""
        for i, v in enumerate(real_videos, 1):
            video_context += f"Видео {i}: {v['title']}\nОписание: {v['description']}\n\n"
            links_list += f"{v['link']}\n"

        # ШАГ 3: Генерация отчета по твоей новой структуре
        final_prompt = f"""
Ты — аналитическая станция The Weit. 
Проведи глубокий бизнес-разбор на основе 10 реальных YouTube-роликов:

{video_context}

ВЫДАЙ ОТЧЕТ СТРОГО ПО ЭТОМУ ФОРМАТУ:

### 🎬 УСПЕШНЫЕ РОЛИКИ ХАРАКТЕРИЗУЮТСЯ:
**Сюжет:** [Детальный разбор структуры]
**Смысловая нагрузка:** [Ключевые идеи]
**Драматургия:** [Как удерживается внимание]
**Длительность:** [Оптимальное время]
**Видеоряд:** [Визуал и монтаж]
**Озвучка:** [Работа со звуком]
**Другие особенности:** [Уникальные фишки]
**Ключевой фактор успеха:** [Почему это смотрят]

**Вывод:** [Бизнес-рекомендация]

---APPLIED_MATERIAL---
### 📂 ПРИКЛАДНОЙ МАТЕРИАЛ:
Ссылки на видео, которые были проанализированы:
{links_list}
"""
        
        response = model.generate_content(final_prompt)
        return response.text
            
    except Exception as e:
        return f"❌ Ошибка системы: {str(e)}"