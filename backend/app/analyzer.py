import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # Сервер подтвердил, что видит эту переменную. Берем её.
    api_key = os.environ.get("GOOGLE_API_KEY")

    # ДИАГНОСТИКА
    if not api_key:
        key_debug = "GOOGLE_API_KEY НЕ НАЙДЕН (Хотя должен быть!)"
    else:
        visible_part = api_key[:5]
        length = len(api_key)
        key_debug = f"Вижу GOOGLE_API_KEY: '{visible_part}...' (Всего: {length} симв.)"

    try:
        if not api_key:
            raise ValueError("Ключ отсутствует")

        genai.configure(api_key=api_key)
        
        # Модель
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
        print(f"❌ ERROR: {str(e)}")
        return f"ОШИБКА: {str(e)} | {key_debug}"
