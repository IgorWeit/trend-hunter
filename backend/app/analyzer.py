import os
import google.generativeai as genai

def get_best_available_model():
    """Автоматически находит лучшую доступную модель для твоего ключа"""
    try:
        # Получаем все модели, доступные твоему ключу
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Твой список приоритетов (от лучшей к просто рабочей)
        priority_list = [
            'models/gemini-1.5-flash',
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-pro',
            'models/gemini-1.0-pro'
        ]
        
        # Ищем совпадение
        for model_name in priority_list:
            if model_name in available_models:
                return model_name
        
        # Если ничего из списка не нашли, берем первую попавшуюся рабочую
        return available_models[0] if available_models else None
    except Exception as e:
        print(f"Ошибка при поиске моделей: {e}")
        return None

def analyze_trend(data):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key: return "ОШИБКА: API ключ не найден."

    try:
        genai.configure(api_key=api_key)
        
        # ШАГ 1: Проверка и выбор доступной модели
        selected_model = get_best_available_model()
        
        if not selected_model:
            return "ОШИБКА: Вашему API ключу не доступна ни одна модель генерации."

        # ШАГ 2: Настройка инструментов (Search Grounding)
        tools = [{"google_search_retrieval": {}}]
        
        model = genai.GenerativeModel(
            model_name=selected_model,
            tools=tools
        )
        
        # ШАГ 3: Запуск анализа
        prompt = f"""
        Ты — аналитик The Weit. Проведи поиск по запросу: "{data}"
        Используй Google Search для поиска 50 реальных источников.
        Выдай таблицу метрик, разбор стратегии и ссылки на реальные видео.
        ---APPLIED_MATERIAL--- (ссылки в конце)
        """
        
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Ошибка системы: {str(e)}"