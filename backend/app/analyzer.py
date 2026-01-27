import os
import google.generativeai as genai
from dotenv import load_dotenv

# Пытаемся загрузить .env (для локальной разработки)
load_dotenv()

def analyze_trend(video_data_text):
    # Читаем ключ внутри функции, чтобы он подхватился даже если задан позже
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        # Пытаемся найти альтернативные имена, вдруг ты назвал его иначе
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        # Выводим список того, что видит сервер (для отладки), но скрываем значения
        env_vars = ", ".join([k for k in os.environ.keys()])
        print(f"❌ ОШИБКА: Ключ не найден. Вижу такие переменные: {env_vars}")
        return "Error: System variable 'GEMINI_API_KEY' is missing on Render. Check Environment tab."

    try:
        genai.configure(api_key=api_key)
        
        target_model_name = 'gemini-1.5-flash' # Пробуем быструю модель по умолчанию
        
        # Проверка доступных моделей (упрощено)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5' in m.name or 'gemini-pro' in m.name:
                    target_model_name = m.name
                    break

        model = genai.GenerativeModel(target_model_name)
        
        prompt = f"""
        Analyze this trend category: "{video_data_text}".
        Provide a strategy in Russian:
        1. Hook (How to start).
        2. Visuals (What to show).
        3. Why it goes viral.
        Keep it concise.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"❌ ОШИБКА AI: {str(e)}")
        return f"AI Error: {str(e)}"
