import os
import google.generativeai as genai

# УБИРАЕМ load_dotenv(). 
# Теперь код не будет шариться по дискам в поисках скрытых файлов.
# from dotenv import load_dotenv
# load_dotenv()

def analyze_trend(video_data_text):
    # Берем напрямую из переменных системы
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Запасной вариант
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")

    # ДИАГНОСТИКА 2.0
    if not api_key:
        key_debug = "КЛЮЧ НЕ НАЙДЕН (None)"
    else:
        visible_part = api_key[:5] # Покажем 5 букв
        length = len(api_key)
        key_debug = f"Вижу ключ: '{visible_part}...' (Всего: {length} симв.)"

    try:
        if not api_key:
            # Выведем список ВСЕХ доступных переменных (только названия), чтобы понять, что видит сервер
            all_vars = ", ".join(list(os.environ.keys()))
            raise ValueError(f"Переменная пуста. Доступные переменные: {all_vars}")

        genai.configure(api_key=api_key)
        
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
        print(f"❌ DEBUG: {key_debug}")
        print(f"❌ ERROR: {str(e)}")
        return f"ОШИБКА: {str(e)} | {key_debug}"
