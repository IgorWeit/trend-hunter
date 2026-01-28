import os
import google.generativeai as genai

def analyze_trend(data):
    api_key = os.environ.get("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Ты — ведущий аналитик FastMoss. Проанализируй данные: {data}
    
    ВЫДАЙ ОТВЕТ СТРОГО В ТАКОМ ФОРМАТЕ:
    
    | Показатель | Значение |
    | :--- | :--- |
    | Viral Score | 9/10 |
    | Товарная ниша | [Категория] |
    | Средняя вовлеченность | 8.5% |
    | Постов проанализировано | 50 |
    
    Затем добавь детальный текстовый отчет с анализом стратегии и рекомендациями.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Ошибка AI: {str(e)}"
