import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def analyze_trend(video_data_text):
    # 1. Пытаемся найти ключ под разными именами
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")

    # 2. Формируем отчет о ключе (для отладки), скрывая сам секрет
    if not api_key:
        key_debug = "КЛЮЧ НЕ НАЙДЕН (None)"
    else:
        # Показываем первые 4 символа и общую длину
        visible_part = api_key[:4]
        length = len(api_key)
        key_debug = f"Ключ найден: '{visible_part}...' (Длина: {length} симв.)"

    try:
        if not api_key:
            raise ValueError("Переменная окружения пуста")

        # Принудительная конфигурация
        genai.configure(api_key=api_key)
        
        # Выбираем модель
        target_model = 'gemini-1.5-flash'
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5' in m.name:
                    target_model = m.name
                    break

        model = genai.GenerativeModel(target_model)
        
        prompt = f"Analyze market strategy for: {video_data_text}. Answer in Russian. Short bullet points."
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"❌ DEBUG INFO: {key_debug}")
        print(f"❌ ERROR: {str(e)}")
        # Возвращаем эту инфу на фронтенд, чтобы ты увидел её в браузере
        return f"ОШИБКА: {str(e)} | ДИАГНОСТИКА: {key_debug}"
