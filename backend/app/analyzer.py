import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # 1. Ищем ключ в любом из возможных карманов
    api_key = os.environ.get("FINAL_KEY")
    key_source = "FINAL_KEY"

    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
        key_source = "GEMINI_API_KEY"
    
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")
        key_source = "GOOGLE_API_KEY"

    # ДИАГНОСТИКА
    if not api_key:
        # Если вообще ничего не нашли - выводим список того, что есть
        env_dump = ", ".join(sorted(list(os.environ.keys())))
        return f"ОШИБКА: Ни один ключ не найден. Вижу переменные: {env_dump}"
    else:
        # Если нашли - покажем какой, и первые 4 буквы (чтобы убедиться, что это AIza)
        visible_part = api_key[:4]
        debug_info = f"Использую {key_source} ('{visible_part}...')"

    try:
        genai.configure(api_key=api_key)
        
        # 2. Безопасный выбор модели (пробуем Pro, она надежнее)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"Analyze market strategy for: {video_data_text}. Answer in Russian. Short bullet points."
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        # Если ошибка 404 - значит модель не та, но ключ верный.
        # Если ошибка 400 - значит ключ битый.
        return f"ОШИБКА AI: {str(e)} | {debug_info}"
