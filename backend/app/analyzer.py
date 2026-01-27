import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # Берем нашу новую чистую переменную
    api_key = os.environ.get("FINAL_KEY")

    try:
        if not api_key:
            raise ValueError("FINAL_KEY не найден в настройках Render")

        genai.configure(api_key=api_key)
        
        # ИСПОЛЬЗУЕМ СТАНДАРТНУЮ МОДЕЛЬ
        # gemini-1.5-flash иногда недоступна на бесплатном тарифе или в v1beta
        # gemini-pro - это "автомат Калашникова", работает везде.
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"Analyze market strategy for: {video_data_text}. Answer in Russian. Short bullet points."
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"ОШИБКА AI: {str(e)}"
