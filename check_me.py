import os
import google.generativeai as genai
from dotenv import load_dotenv

# Загружаем ключ из .env (если он там есть)
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("❌ ОШИБКА: API_KEY не найден в переменных окружения.")
else:
    genai.configure(api_key=api_key)
    print("--- СПИСОК ДОСТУПНЫХ МОДЕЛЕЙ ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"ID: {m.name:35} | Display: {m.display_name}")
    except Exception as e:
        print(f"❌ Ошибка при запросе к API: {e}")