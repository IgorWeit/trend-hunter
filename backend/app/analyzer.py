import os
import google.generativeai as genai

def analyze_trend(video_data_text):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "ОШИБКА: Ключ не найден."

    try:
        genai.configure(api_key=api_key)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        selected = next((m for m in ['models/gemini-1.5-pro', 'models/gemini-1.5-flash'] if m in available_models), available_models[0])

        model = genai.GenerativeModel(selected)
        
        prompt = f"""
        Ты — аналитик FastMoss. Проанализируй данные: {video_data_text}
        Ответь СТРОГО в формате Markdown таблицы с колонками:
        | Показатель | Значение | Аналитический инсайт |
        | :--- | :--- | :--- |
        | Viral Score | [0-10] | Почему такая оценка? |
        | Товарная ниша | [Название] | Какой потенциал в TikTok Shop? |
        | Крючок (Hook) | [Тип] | На чем держится внимание? |
        | Монетизация | [Метод] | Как на этом делают деньги? |
        
        В конце добавь краткий текстовый вывод "Бизнес-вердикт".
        """
        
        response = model.generate_content(prompt)
        return f"### Аналитика FastMoss\n\n{response.text}"
        
    except Exception as e:
        return f"ОШИБКА: {str(e)}"
