import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    secret_path = '/etc/secrets/google_key'
    file_content = "ФАЙЛ НЕ ПРОЧИТАН"
    source = "НЕИЗВЕСТНО"
    
    # 1. Читаем файл и сохраняем то, что видим (для отчета)
    if os.path.exists(secret_path):
        with open(secret_path, 'r') as f:
            raw_content = f.read()
            # Показываем первые 10 и последние 5 символов
            start = raw_content[:10]
            end = raw_content[-5:] if len(raw_content) > 5 else ""
            file_content = f"'{start}...{end}' (Длина: {len(raw_content)})"
            
            # Используем это как ключ
            api_key = raw_content.strip()
            source = f"Файл {secret_path}"
    else:
        # Если файла нет, проверяем переменную (на всякий случай)
        api_key = os.environ.get("GOOGLE_API_KEY")
        source = "Переменная GOOGLE_API_KEY"
        if api_key:
            file_content = f"'{api_key[:10]}...'"
        else:
            file_content = "ПУСТО"

    # 2. Формируем отчет ДО того, как упадем
    debug_info = (
        f"\n\n--- ЭКСПЕРТИЗА ---\n"
        f"Источник: {source}\n"
        f"ВИЖУ КЛЮЧ: {file_content}\n"
        f"------------------"
    )

    try:
        if not api_key:
            return f"ОШИБКА: Ключ не найден нигде. {debug_info}"

        if api_key.startswith("ghp_"):
            return f"🚨 ВНИМАНИЕ: Сервер видит ключ GitHub! {debug_info}"

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Analyze: {video_data_text}. Russian. Short.")
        return response.text
        
    except Exception as e:
        return f"ОШИБКА AI: {str(e)} {debug_info}"
