import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "ОШИБКА: Ключ не найден в настройках сервера."

    try:
        genai.configure(api_key=api_key)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Выбираем лучшую доступную модель
        priority = ['models/gemini-1.5-pro', 'models/gemini-1.5-flash']
        selected = next((m for m in priority if m in available_models), None) or (available_models[0] if available_models else None)

        model = genai.GenerativeModel(selected)
        
        # Твоя новая бизнес-задача для AI
        prompt = f"""
        Ты — эксперт по закупкам в Китае, логистике (ВЭД) и продаже товаров на маркетплейсах.
        Проанализируй список популярных видео и их тематику: 
        {video_data_text}
        
        Дай профессиональный анализ для CargoProsto:
        1. СУТЬ ТРЕНДА: О чем это и почему люди на этом "повернуты"?
        2. ИДЕИ ДЛЯ ЗАКУПКИ: Какие конкретные товары из этого тренда стоит искать на 1688 или фабриках?
        3. ЛОГИСТИЧЕСКИЙ РИСК: Нюансы доставки (вес, объем, хрупкость, наличие батареек/магнитов).
        4. БИЗНЕС-ВЕРДИКТ: Это долгосрочная ниша или "хайп" на неделю?
        
        Отвечай на русском языке, кратко и тезисно.
        """
        
        response = model.generate_content(prompt)
        return f"*(Анализ на базе модели: {selected})*\n\n{response.text}"
        
    except Exception as e:
        return f"ОШИБКА АНАЛИЗА: {str(e)}"
