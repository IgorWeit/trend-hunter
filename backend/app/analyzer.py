import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    api_key = None
    debug_path = "Не проверялся"
    
    # ЧИТАЕМ ИЗ СЕКРЕТНОГО ФАЙЛА RENDER
    secret_path = '/etc/secrets/google_key'
    
    try:
        if os.path.exists(secret_path):
            with open(secret_path, 'r') as f:
                # strip() удалит пробелы и переносы строк, если они случайно попали
                api_key = f.read().strip()
            debug_path = f"Файл найден: {secret_path}"
        else:
            debug_path = f"Файл НЕ найден: {secret_path}"
            
    except Exception as e:
        debug_path = f"Ошибка чтения файла: {str(e)}"

    # Если файла нет, пробуем старый добрый GOOGLE_API_KEY как запасной вариант
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")

    try:
        if not api_key:
            raise ValueError(f"Ключ не добыт. Статус файла: {debug_path}")

        # Проверка на ghp_ (чтобы ты сразу увидел, если старый ключ всё еще лезет)
        if api_key.startswith("ghp_"):
            return f"ОШИБКА: Это ключ от GitHub (ghp_), а не от Google! Проверь файл {secret_path}."

        genai.configure(api_key=api_key)
        
        # Используем gemini-pro как самую стабильную
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"Analyze market strategy for: {video_data_text}. Answer in Russian. Short bullet points."
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        # Показываем первые 4 символа ключа для диагностики
        key_preview = api_key[:4] if api_key else "None"
        return f"ОШИБКА AI: {str(e)} | Ключ: {key_preview}... | Файл: {debug_path}"
