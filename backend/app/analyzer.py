
import google.generativeai as genai



def analyze_trend(video_data_text):

    # --- ХАРДКОД (ВРЕМЕННО) ---

    # Мы вписываем ключ прямо сюда, чтобы исключить любые ошибки сервера.

    # Вставь свой ключ AIza... внутрь кавычек ниже:

    api_key = "AIzaSyCW29jEFUUHLBLZz_PJgpxfwbzbRlck6R0" 

    

    # ПРОВЕРКА НА БЕРЕГУ

    if "ghp_" in api_key:

        return "СТОП! Ты случайно вставил сюда ключ от Гитхаба (ghp_)! Замени его на AIza."



    try:

        genai.configure(api_key=api_key)

        

        # Берем модель gemini-pro

        model = genai.GenerativeModel('gemini-pro')

        

        prompt = f"Analyze market strategy for: {video_data_text}. Answer in Russian. Short bullet points."

        

        response = model.generate_content(prompt)

        return response.text

        

    except Exception as e:

        return f"ОШИБКА AI: {str(e)}"

