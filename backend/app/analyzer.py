import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # Берем ключ из переменной (ты его уже прописал в 'trend-hunter', так что сработает)
    api_key = os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        return "ОШИБКА: Ключ GOOGLE_API_KEY не найден."

    try:
        genai.configure(api_key=api_key)
        
        # Используем новейшую модель 1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Проанализируй рыночную стратегию для следующего контента: {video_data_text}. Ответь на русском языке, кратко, тезисами."
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"ОШИБКА AI: {str(e)}"
