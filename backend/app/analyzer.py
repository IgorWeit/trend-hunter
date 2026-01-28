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
        
        # Логика в стиле FastMoss (TikTok Shop & Trend Analytics)
        prompt = f"""
        Ты — ведущий аналитик платформы мониторинга трендов, аналогичной FastMoss.
        Проанализируй следующие данные по контенту: 
        {video_data_text}
        
        Подготовь отчет в формате FastMoss Analytics:
        1. ТРЕНДОВЫЙ РЕЙТИНГ (Viral Score): Оценка потенциала виральности контента (1-10) и причины роста.
        2. PRODUCT INSIGHTS: Какие конкретные категории товаров или ниши продвигаются? Оцени их востребованность.
        3. CONTENT STRATEGY: Какие хуки (hooks) и визуальные приемы используют авторы для удержания внимания и конверсии?
        4. МОНЕТИЗАЦИЯ: Как данный тренд связан с продажами (TikTok Shop, Affiliate-ссылки, трафик на лендинги)?
        
        Отвечай профессионально, используя терминологию e-commerce аналитики.
        """
        
        response = model.generate_content(prompt)
        return f"*(FastMoss Style Analysis | Model: {selected})*\n\n{response.text}"
        
    except Exception as e:
        return f"ОШИБКА АНАЛИЗА: {str(e)}"
