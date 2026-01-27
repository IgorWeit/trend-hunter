import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # Теперь ищем только ОДНУ переменную. 
    # Мы почистили Render, так что конфликтов не будет.
    api_key = os.environ.get("GEMINI_API_KEY")

    try:
        if not api_key:
            raise ValueError("Ключ не найден в Environment")

        genai.configure(api_key=api_key)
        
        # Модель
        target_model = 'gemini-1.5-flash'
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5' in m.name:
                    target_model = m.name
                    break

        model = genai.GenerativeModel(target_model)
        
        prompt = f"Analyze market strategy for: {video_data_text}. Answer in Russian. Short bullet points."
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"ОШИБКА AI: {str(e)}"
