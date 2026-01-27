import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def analyze_trend(video_data_text):
    if not api_key:
        return "Error: API Key not found in .env"

    try:
        genai.configure(api_key=api_key)
        
        # --- БЛОК АВТОПОИСКА МОДЕЛИ ---
        # Мы не гадаем название, а берем первую доступную из списка
        target_model_name = None
        
        print("🔍 Ищу доступные модели...")
        for m in genai.list_models():
            # Ищем модели, которые умеют генерировать текст ('generateContent')
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini' in m.name:
                    target_model_name = m.name
                    print(f"✅ Выбрана модель: {target_model_name}")
                    break # Берем первую найденную и выходим
        
        if not target_model_name:
            # Если автопоиск не сработал, пробуем самую старую и надежную как запасной вариант
            target_model_name = 'models/gemini-pro'
            print("⚠️ Автопоиск не дал результатов. Пробую models/gemini-pro")
        # ------------------------------

        model = genai.GenerativeModel(target_model_name)
        
        prompt = f"""
        Analyze this trend category: "{video_data_text}".
        Provide a strategy in Russian:
        1. Hook (How to start).
        2. Visuals (What to show).
        3. Why it goes viral.
        Keep it concise.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"❌ ОШИБКА AI: {str(e)}")
        return f"AI Error: {str(e)}"