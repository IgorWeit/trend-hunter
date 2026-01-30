import os
import google.generativeai as genai
import time

def analyze_trend(data):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key: 
        return "ОШИБКА: API ключ не найден."
    
    try:
        genai.configure(api_key=api_key)
        all_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # СТРОГИЙ ПРИОРИТЕТ: 1.5-flash — наш спаситель (1500 запросов в день)
        # Мы убираем 2.0 и 2.5, так как они блокируют работу на Free Tier
        priority_order = [
            'models/gemini-1.5-flash',    # Самая высокая квота
            'models/gemini-1.5-flash-8b', 
            'models/gemini-1.5-pro',      # 50 запросов в день
            'models/gemini-1.0-pro',      # Старая, но надежная
        ]
        
        available_models = []
        model_names_in_system = [m.name for m in all_models]

        for priority in priority_order:
            if priority in model_names_in_system:
                available_models.append(priority)

        if not available_models:
            # Если точных совпадений нет, берем любую, кроме 2.5
            available_models = [m.name for m in all_models if '2.5' not in m.name]

        last_error = None
        
        for model_name in available_models:
            try:
                print(f"✅ The Weit запускает: {model_name}")
                model = genai.GenerativeModel(model_name=model_name)
                
                prompt = f"""
Ты — аналитическая станция The Weit. Проанализируй данные: {data}

ОБЯЗАТЕЛЬНО ВКЛЮЧИ ЭТУ ТАБЛИЦУ В НАЧАЛО:
| Показатель | Значение |
| :--- | :--- |
| Viral Score | [0-10] |
| Товарная ниша | [Название] |
| Средняя вовлеченность | [0.0]% |
| Постов проанализировано | 50 |

### 🎬 РАЗБОР СТРАТЕГИИ
**Сюжет:** [Анализ]
**Ключевой фактор успеха:** [Что сработало]
**Вывод:** [Рекомендация]

---APPLIED_MATERIAL---
Анализ выполнен моделью {model_name}.
"""
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text
                
            except Exception as e:
                error_msg = str(e)
                last_error = error_msg
                
                if "quota" in error_msg.lower() or "429" in error_msg:
                    print(f"⚠️ Модель {model_name} перегружена. Ждем 15 сек...")
                    time.sleep(15)
                    continue  
                else:
                    continue
        
        return f"⚠️ Все рабочие модели (1.5 Flash/Pro) временно недоступны. Ошибка: {last_error}"
        
    except Exception as e:
        return f"❌ Ошибка инициализации: {str(e)}"