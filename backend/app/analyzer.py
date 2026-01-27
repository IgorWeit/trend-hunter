import os
import google.generativeai as genai
import subprocess

def search_for_ghost_key():
    report = []
    found_ghp = False
    
    # 1. ПРОВЕРКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ (Environment)
    report.append("--- [1] Environment Variables ---")
    for key, value in os.environ.items():
        if "API" in key or "KEY" in key or "SECRET" in key:
            if value.startswith("ghp_"):
                report.append(f"🔴 НАЙДЕН ghp_ в переменной: {key}")
                found_ghp = True
            elif value.startswith("AIza"):
                report.append(f"🟢 НАЙДЕН AIza в переменной: {key}")
            else:
                report.append(f"⚪ {key}: (не похож на ключ)")

    # 2. ПРОВЕРКА СКРЫТЫХ ФАЙЛОВ .env
    report.append("\n--- [2] Файлы .env ---")
    if os.path.exists(".env"):
        report.append("⚠️ Найден файл .env! Читаю содержимое...")
        try:
            with open(".env", "r") as f:
                content = f.read()
                if "ghp_" in content:
                    report.append("🔴 ВНУТРИ .env ЕСТЬ 'ghp_'!")
                    found_ghp = True
                else:
                    report.append("⚪ Файл .env чист.")
        except:
            report.append("Ошибка чтения .env")
    else:
        report.append("✅ Файла .env нет.")

    # 3. ПРОВЕРКА GIT CONFIG (Частая причина!)
    report.append("\n--- [3] Git Config ---")
    try:
        # Иногда ключ сохраняется в url репозитория: https://ghp_...@github.com/...
        git_config = subprocess.check_output(["git", "config", "--list"], text=True)
        if "ghp_" in git_config:
            report.append("🔴 НАЙДЕН 'ghp_' в настройках GIT! (Возможно в remote origin url)")
            found_ghp = True
        else:
            report.append("✅ Git config чист.")
    except:
        report.append("Не удалось проверить Git config.")

    return "\n".join(report), found_ghp

def analyze_trend(video_data_text):
    # Запускаем диагностику
    debug_report, ghost_found = search_for_ghost_key()
    
    # Если нашли ghp - возвращаем отчет, чтобы ты увидел, где он
    if ghost_found:
        return f"🚨 ПРИЗРАК НАЙДЕН! 🚨\n\n{debug_report}"
    
    # Если ghp нет, пробуем работать с тем, что есть
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("FINAL_KEY")
    
    if not api_key:
        return f"ОШИБКА: Ключей нет вообще.\n\n{debug_report}"

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Analyze: {video_data_text}. Russian. Short.")
        return response.text
    except Exception as e:
        return f"ОШИБКА AI: {str(e)}\n\n--- ОТЧЕТ ---\n{debug_report}"
