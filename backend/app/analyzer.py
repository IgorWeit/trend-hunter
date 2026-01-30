import os
import google.generativeai as genai
import time

def analyze_trend(data):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key: 
        return "ОШИБКА: API ключ не найден."
    
    try:
        genai.configure(api_key=api_key)
        
        # ТОЧНЫЙ ПРИОРИТЕТ на основе твоего списка ID
        # Ставим самые "лимитно-выгодные" модели на первые места
        priority_order = [
            'models/gemini-flash-latest',       # Самая стабильная и выносливая
            'models/gemini-2.5-flash-lite',     # Новая Lite с огромными квотами
            'models/gemini-2.0-flash-lite',     # Вторая Lite
            'models/gemini-pro-latest',        # Стабильная Pro
            'models/gemini-3-flash-preview'     # Экспериментальное 3-е поколение
        ]
        
        last_error = None
        for model_id in priority_order:
            try:
                print(f"✅ The Weit Intelligence запускает: {model_id}")
                model = genai.GenerativeModel(model_name=model_id)
                
                prompt = f"""
Ты — аналитическая станция The Weit.
Проанализируй данные: {data}

ОБЯЗАТЕЛЬНО ВКЛЮЧИ ЭТУ ТАБЛИЦУ В НАЧАЛО:
| Показатель | Значение |
| :--- | :--- |
| Viral Score | [0-10] |
| Товарная ниша | [Название] |
| Средняя вовлеченность | [0.0]% |
| Постов проанализировано | 50 |

---APPLIED_MATERIAL---
Анализ выполнен через узел {model_id}.
"""
                response = model.generate_content(prompt)
                if response and response.text:
                    print(f"🎯 Успех! Модель {model_id} сработала.")
                    return response.text
                
            except Exception as e:
                error_msg = str(e)
                last_error = error_msg
                # Если видим 429 (лимит), ждем немного и пробуем следующую
                if "429" in error_msg or "quota" in error_msg.lower():
                    print(f"⚠️ {model_id} исчерпала минутный лимит. Пробуем следующую...")
                    time.sleep(2) # Небольшая пауза, чтобы не злить API
                    continue
                else:
                    print(f"❌ Ошибка в {model_id}: {error_msg}")
                    continue
        
        return f"⚠️ Все доступные модели перегружены. Попробуйте через 1 минуту. (Ошибка: {last_error})"
        
    except Exception as e:
        return f"❌ Критическая ошибка API: {str(e)}"