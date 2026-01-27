import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # Теперь мы доверяем только GEMINI_API_KEY
    # GOOGLE_API_KEY мы удалили, чтобы не путаться
    api_key = os.environ.get("GEMINI_API_KEY")

    try:
        if not api_key:
            # Если ключа нет - значит в Environment пусто
            raise ValueError("GEMINI_API_KEY не найден. Проверьте Render.")

        genai.configure(api_key=api_key)
        
        # Используем самую надежную модель
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"Analyze market strategy for: {video_data_text}. Answer in Russian. Short bullet points."
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"ОШИБКА AI: {str(e)}"
