import os
import google.generativeai as genai
from google.generativeai import types

def get_best_available_model():
    """Автоматически находит лучшую доступную модель"""
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        priority_list = [
            'models/gemini-1.5-flash',
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-pro'
        ]
        for model_name in priority_list:
            if model_name in available_models:
                return model_name
        return available_models[0] if available_models else None
    except Exception:
        return None

def analyze_trend(data):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key: return "ОШИБКА: API ключ не найден."

    try:
        genai.configure(api_key=api_key)
        selected_model = get_best_available_model()
        
        if not selected_model:
            return "ОШИБКА: Доступные модели не найдены."

        # Используем жесткую типизацию Tool для поиска
        # Это исключает ошибку "Unknown field for FunctionDeclaration"
        tools = [types.Tool(google_search=types.GoogleSearch())]
        
        model = genai.GenerativeModel(
            model_name=selected_model,
            tools=tools
        )
        
        prompt = f"""
        Ты — аналитическая станция The Weit. Твой запрос: "{data}"
        
        ЗАДАЧА:
        1. Используй Google Search для поиска 50 реальных роликов и трендов.
        2. Сформируй анализ на базе ТОЛЬКО найденных данных.
        3. Выведи ссылки на YouTube в конце.

        ФОРМАТ ОТЧЕТА:
        ### 📊 ТАБЛИЦА МЕТРИК
        | Metric | Value | Comparison |
        | :--- | :--- | :--- |
        | Viral Score | [0-10] | [Оценка] |
        | Product Niche | [Ниша] | [Тренд] |
        | Engagement | [0.0]% | [Vs 5.2%] |
        | Data Sources | 50 | [Verified] |

        ### 🎬 РАЗБОР СТРАТЕГИИ
        **Сюжет:** ...
        **Смысловая нагрузка:** ...
        **Драматургия:** ...
        **Видеоряд:** ...
        **Озвучка:** ...
        **Ключевой фактор успеха:** ...
        **Вывод:** ...

        ---APPLIED_MATERIAL---
        **РЕАЛЬНЫЕ ИСТОЧНИКИ АНАЛИЗА:**
        (Выведи список из 5-10 реальных URL-адресов YouTube, найденных поиском)
        """
        
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Критический сбой API (Grounding): {str(e)}"