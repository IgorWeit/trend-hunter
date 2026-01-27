import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    # Получаем СПИСОК всех имен переменных (без значений, чтобы безопасно)
    all_keys = sorted(list(os.environ.keys()))
    
    # Ищем наш ключ среди них (даже с ошибками в регистре)
    found_candidates = []
    for key in all_keys:
        if "TITAN" in key or "GEMINI" in key or "GOOGLE" in key:
            # Показываем имя и первые 4 символа значения, чтобы понять, что внутри
            val = os.environ[key]
            preview = val[:4] if val else "EMPTY"
            found_candidates.append(f"{key}='{preview}...'")

    # Формируем отчет
    env_dump = ", ".join(all_keys)
    candidates_dump = "\n".join(found_candidates)

    if not found_candidates:
        return f"⛔ КЛЮЧЕЙ НЕТ ВООБЩЕ.\nСервер видит вот эти переменные:\n[{env_dump}]"
    
    # Если нашли хоть что-то похожее на ключ - пробуем использовать
    try:
        # Берем первый найденный
        key_name = found_candidates[0].split('=')[0]
        api_key = os.environ[key_name]
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Analyze: {video_data_text}. Russian. Short.")
        return response.text

    except Exception as e:
        return f"ОШИБКА AI: {str(e)}\n\n--- НАЙДЕННЫЕ КАНДИДАТЫ ---\n{candidates_dump}\n\n--- ВСЕ ПЕРЕМЕННЫЕ ---\n{env_dump}"
