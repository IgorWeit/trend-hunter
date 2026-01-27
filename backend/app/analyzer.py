import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # 1. Получаем ключ (теперь безопасно)
    api_key = os.environ.get("GEMINI_API_KEY")

    try:
        if not api_key:
            raise ValueError("Ключ не найден в Environment")

        genai.configure(api_key=api_key)
        
        # 2. УМНЫЙ ПОДБОР МОДЕЛИ
        # Мы не гадаем, а спрашиваем у Google: "Что у тебя есть?"
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        target_model = None
        
        # Приоритет 1: Flash (самая быстрая)
        for m in available_models:
            if 'flash' in m and '1.5' in m:
                target_model = m
                break
        
        # Приоритет 2: Pro (если Flash нет)
        if not target_model:
            for m in available_models:
                if 'pro' in m:
                    target_model = m
                    break
                    
        # Приоритет 3: Хоть что-нибудь
        if not target_model and available_models:
            target_model = available_models[0]

        if not target_model:
            return "ОШИБКА: Не найдено ни одной доступной модели AI."

        # print(f"DEBUG: Использую модель {target_model}") # Для отладки

        model = genai.GenerativeModel(target_model)
        
        prompt = f"Analyze market strategy for: {video_data_text}. Answer in Russian. Short bullet points."
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"ОШИБКА AI: {str(e)}"
