import os
import google.generativeai as genai
import time

def analyze_trend(data):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key: 
        return "ОШИБКА: API ключ не найден."
    
    try:
        genai.configure(api_key=api_key)
        
        # Получаем список доступных моделей
        all_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # ПРИОРИТЕТ МОДЕЛЕЙ (от самой быстрой с большими лимитами к мощной)
        # Flash обычно имеет больший лимит запросов, чем Pro
        priority_order = [
            'gemini-2.0-flash',       # Новейшая Flash (самые большие лимиты)
            'gemini-1.5-flash',       # Flash (большие лимиты)
            'gemini-1.5-flash-8b',    # Легкая Flash (огромные лимиты)
            'gemini-1.5-pro',         # Pro (меньше лимитов, но мощнее)
            'gemini-pro',             # Старая Pro
        ]
        
        # Ищем доступные модели по приоритету
        available_models = []
        for model_obj in all_models:
            model_full_name = model_obj.name
            for priority in priority_order:
                if priority in model_full_name:
                    available_models.append({
                        'name': model_full_name,
                        'priority': priority_order.index(priority),
                        'display_name': priority
                    })
                    break
        
        # Сортируем по приоритету
        available_models.sort(key=lambda x: x['priority'])
        
        if not available_models:
            return "ОШИБКА: Нет доступных моделей Gemini."
        
        print(f"🔍 Доступные модели (по приоритету):")
        for m in available_models:
            print(f"  - {m['display_name']} ({m['name']})")
        
        # ПЫТАЕМСЯ ИСПОЛЬЗОВАТЬ МОДЕЛИ ПО ОЧЕРЕДИ
        last_error = None
        
        for model_info in available_models:
            model_name = model_info['name']
            display_name = model_info['display_name']
            
            try:
                print(f"✅ Пробуем модель: {display_name}")
                
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
                
                if response and response.text:
                    print(f"✅ Успешно использована модель: {display_name}")
                    return response.text
                
            except Exception as e:
                error_msg = str(e)
                last_error = error_msg
                
                # Проверяем тип ошибки
                if "quota" in error_msg.lower() or "429" in error_msg or "resource" in error_msg.lower():
                    print(f"⚠️ {display_name}: Превышен лимит, переключаемся на следующую модель...")
                    time.sleep(1)  # Небольшая задержка перед следующей попыткой
                    continue  # Пробуем следующую модель
                elif "api key" in error_msg.lower() or "401" in error_msg or "403" in error_msg:
                    # Проблема с ключом - нет смысла пробовать другие модели
                    return f"⚠️ Проблема с API ключом: {error_msg}"
                else:
                    # Неизвестная ошибка - пробуем следующую модель
                    print(f"⚠️ {display_name}: {error_msg}")
                    continue
        
        # Если все модели исчерпаны
        return f"""⚠️ Все доступные модели Gemini исчерпали лимиты.

**Что делать:**
1. Подождите 1-2 минуты и попробуйте снова
2. Проверьте квоты в [Google AI Studio](https://aistudio.google.com/app/apikey)
3. Рассмотрите возможность upgrade аккаунта

**Последняя ошибка:** {last_error}

**Попытались использовать:** {', '.join([m['display_name'] for m in available_models])}
"""
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Критическая ошибка: {error_msg}")
        
        return f"❌ Критическая ошибка API: {error_msg}"


# ДОПОЛНИТЕЛЬНО: Функция для проверки доступных моделей (можно вызвать отдельно)
def check_available_models():
    """
    Вспомогательная функция для проверки доступных моделей
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "API ключ не найден"
    
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        
        result = "📋 Доступные модели Gemini:\n\n"
        
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                result += f"✅ {m.name}\n"
                result += f"   Методы: {', '.join(m.supported_generation_methods)}\n"
                result += f"   Лимиты: {m.rate_limit if hasattr(m, 'rate_limit') else 'N/A'}\n\n"
        
        return result
        
    except Exception as e:
        return f"Ошибка: {str(e)}"