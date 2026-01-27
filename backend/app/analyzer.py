
import google.generativeai as genai



def analyze_trend(video_data_text):

    # ХАРДКОД. Мы устали бороться с сервером.

    # Вставь свой ключ AIza... прямо сюда внутри кавычек:

    api_key = "AIzaSyA1OchfTQx5YORPXrvvtq05GQGoMtM5NNc"



    try:

        genai.configure(api_key=api_key)

        

        # Модель

        target_model = 'gemini-1.5-flash'

        for m in genai.list_models():

            if 'generateContent' in m.supported_generation_methods:

                if 'gemini-1.5' in m.name:

                    target_model = m.name

                    break



        model = genai.GenerativeModel(target_model)

        

        prompt = f"Analyze market strategy for: {video_data_text}. Answer in Russian. Short bullet points."

        

        response = model.generate_content(prompt)

        return response.text

        

    except Exception as e:

        return f"ОШИБКА: {str(e)}"

