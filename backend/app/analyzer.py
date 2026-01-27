import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # Пытаемся взять ключ
    api_key = os.environ.get("GEMINI_API_KEY")

    # СТУКАЧ: Собираем список всех переменных, которые видит сервер
    # Мы сортируем их, чтобы тебе было легче искать глазами
    env_keys = sorted(list(os.environ.keys()))
    env_list_str = ", ".join(env_keys)

    try:
        if not api_key:
            # Выводим ошибку и СПИСОК ПЕРЕМЕННЫХ
            raise ValueError(f"КЛЮЧА НЕТ. Сервер видит только эти переменные: [{env_list_str}]")

        genai.configure(api_key=api_key)
        
        # Подбор модели
        target_model = 'gemini-1.5-flash'
        # (Упрощенная логика для теста, главное - авторизация)
        
        model = genai.GenerativeModel(target_model)
        prompt = f"Analyze: {video_data_text}. Russian. Short."
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"ОШИБКА: {str(e)}"
