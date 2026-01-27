import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # Берем ключ ТОЛЬКО из защищенных настроек Render
    api_key = os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        return "ОШИБКА: Ключ не найден в Environment Variables на Render."

    try:
        genai.configure(api_key=api_key)
        
        # Динамический поиск лучшей модели
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        priority = ['models/gemini-1.5-pro', 'models/gemini-1.5-flash']
        selected = next((m for m in priority if m in available_models), None) or (available_models[0] if available_models else None)

        if not selected:
            return "ОШИБКА: Нет доступных моделей для этого ключа."

        model = genai.GenerativeModel(selected)
        response = model.generate_content(f"Проанализируй рыночную стратегию для: {video_data_text}. Ответь на русском языке.")
        
        return f"*(Модель: {selected})*\n\n{response.text}"
        
    except Exception as e:
        return f"ОШИБКА AI: {str(e)}"
