import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "ОШИБКА: Ключ не найден."

    try:
        genai.configure(api_key=api_key)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        selected = next((m for m in ['models/gemini-1.5-pro', 'models/gemini-1.5-flash'] if m in available_models), available_models[0])

        model = genai.GenerativeModel(selected)
        
        # Логика в стиле FastMoss
        prompt = f"""
        Ты — ведущий аналитик платформы мониторинга трендов (аналог FastMoss).
        Проанализируй данные по контенту: 
        {video_data_text}
        
        Дай отчет в формате FastMoss Analytics:
        1. ТРЕНДОВЫЙ РЕЙТИНГ: Оценка потенциала виральности (1-10).
        2. АНАЛИЗ ТОВАРА (Product Insight): Какие категории товаров доминируют в этом контенте?
        3. СТРАТЕГИЯ КРЕАТИВА: Какие визуальные приемы используют авторы для удержания внимания?
        4. МОНЕТИЗАЦИЯ: Как этот тренд конвертируется в продажи (TikTok Shop, партнерки, прямой трафик)?
        
        Отвечай профессионально, используя терминологию e-commerce аналитики.
        """
        
        response = model.generate_content(prompt)
        return f"*(FastMoss Style Analysis | Model: {selected})*\n\n{response.text}"
        
    except Exception as e:
        return f"ОШИБКА: {str(e)}"
