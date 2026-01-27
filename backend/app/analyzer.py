import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # Теперь берем ключ ТОЛЬКО из настроек сервера
    api_key = os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        return "ОШИБКА: Ключ не найден в настройках сервера (Environment Variables)."

    try:
        genai.configure(api_key=api_key)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        priority_list = [
            'models/gemini-1.5-pro',
            'models/gemini-1.5-pro-latest', 
            'models/gemini-1.5-flash',
            'models/gemini-1.5-flash-latest'
        ]
        
        selected_model = next((m for m in priority_list if m in available_models), None) or (available_models[0] if available_models else None)

        if not selected_model:
            return "ОШИБКА: Нет доступных моделей."

        model = genai.GenerativeModel(selected_model)
        prompt = f"Проанализируй рыночную стратегию: {video_data_text}. Ответь на русском языке."
        
        response = model.generate_content(prompt)
        return f"*(Модель: {selected_model})*\n\n{response.text}"
        
    except Exception as e:
        return f"ОШИБКА АНАЛИЗА: {str(e)}"
