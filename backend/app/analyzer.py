import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # Сервер сказал, что у него есть GOOGLE_API_KEY. Используем его.
    api_key = os.environ.get("GOOGLE_API_KEY")

    try:
        if not api_key:
            raise ValueError("Ключ не найден (даже GOOGLE_API_KEY)")

        genai.configure(api_key=api_key)
        
        # Автопоиск рабочей модели (чтобы не было ошибки 404)
        target_model = 'gemini-1.5-flash' # Пробуем по умолчанию
        
        # Если API пустит, спросим список моделей
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    if 'gemini-1.5' in m.name:
                        target_model = m.name
                        break
        except:
            pass # Если не получилось получить список, пробуем наугад 'gemini-1.5-flash'

        model = genai.GenerativeModel(target_model)
        
        prompt = f"Analyze market strategy for: {video_data_text}. Answer in Russian. Short bullet points."
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"ОШИБКА AI: {str(e)}"
