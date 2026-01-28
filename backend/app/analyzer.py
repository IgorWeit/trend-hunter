import os
import google.generativeai as genai

def analyze_trend(data):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "ОШИБКА: API ключ не найден."

    try:
        genai.configure(api_key=api_key)
        
        # Получаем список всех доступных моделей для этого ключа
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Ищем лучшую из доступных (Pro -> Flash -> любая работающая)
        if any('models/gemini-1.5-pro' in m for m in models):
            model_name = 'models/gemini-1.5-pro'
        elif any('models/gemini-1.5-flash' in m for m in models):
            model_name = 'models/gemini-1.5-flash'
        else:
            model_name = models[0] if models else None

        if not model_name:
            return "ОШИБКА: Нет доступных моделей Gemini."

        model = genai.GenerativeModel(model_name)
        
        # Промпт уже адаптирован под новые карточки
        prompt = f"""
        Ты — элитный аналитик системы The Weit.
        Проанализируй данные: {data}
        
        ОБЯЗАТЕЛЬНО ВКЛЮЧИ ЭТУ ТАБЛИЦУ В НАЧАЛО:
        | Показатель | Значение |
        | :--- | :--- |
        | Viral Score | [0-10] |
        | Товарная ниша | [Название] |
        | Средняя вовлеченность | [0.0]% |
        | Постов проанализировано | [Число] |
        
        Далее дай глубокий бизнес-анализ на русском языке.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"ОШИБКА СИСТЕМЫ: {str(e)}"
