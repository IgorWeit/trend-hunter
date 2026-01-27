import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # Пытаемся взять ключ из всех возможных мест
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("TITAN_KEY")
    
    # Резервный хардкод (вставь свой AIza сюда для страховки)
    if not api_key or "ghp" in api_key:
        api_key = "ВСТАВЬ_СЮДА_СВОЙ_AIZA_КЛЮЧ"

    try:
        genai.configure(api_key=api_key)
        
        # Пробуем по очереди самые стабильные модели
        for model_name in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
            try:
                model = genai.GenerativeModel(model_name)
                prompt = f"Проанализируй рыночную стратегию для контента: {video_data_text}. Ответь на русском языке."
                response = model.generate_content(prompt)
                return response.text
            except Exception:
                continue # Если модель не найдена, пробуем следующую
        
        return "ОШИБКА: Ни одна из моделей Gemini не доступна в этом регионе или для этого ключа."
        
    except Exception as e:
        return f"ОШИБКА AI: {str(e)}"
