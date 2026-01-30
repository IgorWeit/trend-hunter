import os
import google.generativeai as genai

def analyze_trend(data):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key: 
        return "ОШИБКА: API ключ не найден."
    
    try:
        genai.configure(api_key=api_key)
        
        # Получаем список доступных моделей
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        print(f"🔍 Доступные модели: {models}")
        
        # Ищем модель с поддержкой поиска
        model_name = None
        for m in models:
            if 'gemini-1.5-pro' in m or 'gemini-pro' in m:
                model_name = m
                break
        
        if not model_name:
            for m in models:
                if 'gemini-1.5-flash' in m or 'gemini-flash' in m:
                    model_name = m
                    break
        
        if not model_name and models:
            model_name = models[0]
        
        if not model_name:
            return "ОШИБКА: Нет доступных моделей Gemini."
        
        print(f"✅ Используем модель: {model_name}")
        
        # ИСПРАВЛЕНО: Убираем tools, используем обычный запрос
        model = genai.GenerativeModel(model_name=model_name)
        
        prompt = f"""
Ты — аналитическая станция The Weit.
Проанализируй данные: {data}

ОБЯЗАТЕЛЬНО ВКЛЮЧИ ЭТУ ТАБЛИЦУ В НАЧАЛО:
| Показатель | Значение |
| :--- | :--- |
| Viral Score | [0-10] |
| Товарная ниша | [Название] |
| Средняя вовлеченность | [0.0]% |
| Постов проанализировано | [Число] |

### 🎬 РАЗБОР СТРАТЕГИИ
**Сюжет:** [Анализ структуры контента]
**Смысловая нагрузка:** [Ключевые идеи]
**Драматургия:** [Как удерживается внимание]
**Видеоряд:** [Визуальная составляющая]
**Озвучка:** [Подача информации]
**Ключевой фактор успеха:** [Что сработало]
**Вывод:** [Итоговая рекомендация]

Дай глубокий бизнес-анализ на русском языке.
"""
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Ошибка Gemini: {error_msg}")
        
        # Более детальная обработка ошибок
        if "google_search_retrieval" in error_msg or "google_search" in error_msg:
            return f"⚠️ Ошибка API: Google Search в данный момент недоступен для этой модели. Используется базовый анализ.\n\nОшибка: {error_msg}"
        elif "quota" in error_msg.lower():
            return "⚠️ Превышен лимит запросов к Gemini API. Попробуйте через минуту."
        elif "api key" in error_msg.lower():
            return "⚠️ Проблема с API ключом. Проверьте переменную GOOGLE_API_KEY."
        else:
            return f"Ошибка API: {error_msg}"