import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # Читаем ТОЛЬКО новую переменную.
    # Старые (GOOGLE_API_KEY и т.д.) игнорируем, они отравлены.
    api_key = os.environ.get("TITAN_KEY")

    debug_info = "Ключ TITAN_KEY не найден."
    
    if api_key:
        visible = api_key[:4]
        debug_info = f"Вижу TITAN_KEY: '{visible}...'"
        
        # Сразу проверяем на вирус ghp
        if api_key.startswith("ghp_"):
            return f"ОШИБКА: Даже в TITAN_KEY попал ghp! Это невозможно."

    try:
        if not api_key:
            raise ValueError(f"Переменная пуста. {debug_info}")

        genai.configure(api_key=api_key)
        
        # Используем gemini-pro (самая надежная)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"Analyze market strategy for: {video_data_text}. Answer in Russian. Short bullet points."
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"ОШИБКА AI: {str(e)} | {debug_info}"
