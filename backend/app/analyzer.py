import os
import google.generativeai as genai

def analyze_trend(data):
    api_key = os.environ.get("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Определяем тип запроса
    req_type = data.get('type', 'channel')
    
    if req_type == 'battle':
        q1, q2 = data.get('query1'), data.get('query2')
        prompt = f"""
        Ты аналитик FastMoss. Проведи БИТВУ ТРЕНДОВ между двумя запросами: "{q1}" и "{q2}".
        Сравни их популярность в TikTok и YouTube Shorts.
        Выдай ответ в виде таблицы:
        | Критерий | {q1} | {q2} |
        | :--- | :--- | :--- |
        | Viral Score | [0-10] | [0-10] |
        | Динамика (TikTok) | [Рост/Спад] | [Рост/Спад] |
        | Динамика (YouTube) | [Рост/Спад] | [Рост/Спад] |
        | Товарный потенциал | [Категория] | [Категория] |
        
        Вынеси ВЕРДИКТ: какой тренд сейчас принесет больше денег в TikTok Shop?
        """
    else:
        url = data.get('url', '')
        prompt = f"""
        Проанализируй канал: {url}. 
        Определи контент-стратегию и товарные ниши для TikTok и YouTube одновременно.
        Выдай результат в таблице FastMoss:
        | Показатель | Значение | Инсайт |
        | :--- | :--- | :--- |
        | Viral Score | [0-10] | Почему? |
        | Товарная ниша | [Категория] | Перспектива |
        | Платформа-лидер | [TT или YT] | Где больше вовлеченность? |
        """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Ошибка AI: {str(e)}"
