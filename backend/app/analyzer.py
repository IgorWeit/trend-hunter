import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    # Если в переменной пусто, используем наш временный хардкод
    if not api_key or api_key.startswith("ghp_"):
        api_key = "ТВОЙ_КЛЮЧ_AIza" # Оставь здесь свой ключ, если не уверен в переменной

    try:
        genai.configure(api_key=api_key)
        
        # Используем имя-синоним, оно самое надежное
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"Проанализируй рыночную стратегию для следующего контента: {video_data_text}. Ответь на русском языке, кратко, тезисами."
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"ОШИБКА AI (Model Error): {str(e)}"
