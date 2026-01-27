import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key or "ghp" in api_key:
        api_key = "ВСТАВЬ_СВОЙ_AIZA_КЛЮЧ_СЮДА"

    try:
        genai.configure(api_key=api_key)
        
        # Получаем список всех доступных моделей
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Иерархия качества
        priority_list = [
            'models/gemini-1.5-pro',
            'models/gemini-1.5-pro-latest', 
            'models/gemini-1.5-flash',
            'models/gemini-1.5-flash-latest',
            'models/gemini-pro'
        ]
        
        selected_model = next((m for m in priority_list if m in available_models), None)
        
        if not selected_model:
            selected_model = available_models[0] if available_models else None

        if not selected_model:
            return "ОШИБКА: Нет доступных моделей Gemini."

        model = genai.GenerativeModel(selected_model)
        prompt = f"Проанализируй рыночную стратегию для контента: {video_data_text}. Ответь на русском языке, максимально глубоко и тезисно."
        
        response = model.generate_content(prompt)
        return f"*(Модель: {selected_model})*\n\n{response.text}"
        
    except Exception as e:
        return f"ОШИБКА АНАЛИЗА: {str(e)}"
