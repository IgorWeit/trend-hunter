import os
import google.generativeai as genai

def get_best_available_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        priority = ['models/gemini-1.5-flash', 'models/gemini-1.5-flash-latest', 'models/gemini-1.5-pro']
        for m in priority:
            if m in available_models: return m
        return available_models[0] if available_models else None
    except:
        return "models/gemini-1.5-flash"

def analyze_trend(data):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key: return "ОШИБКА: API ключ не найден."

    try:
        genai.configure(api_key=api_key)
        selected_model = get_best_available_model()

        # ПОПЫТКА 1: Новый формат (google_search)
        try:
            model = genai.GenerativeModel(
                model_name=selected_model,
                tools=[{'google_search': {}}]
            )
            response = model.generate_content(f"Найди 50 видео и проанализируй: {data}")
        except Exception:
            # ПОПЫТКА 2: Классический формат (google_search_retrieval)
            try:
                model = genai.GenerativeModel(
                    model_name=selected_model,
                    tools=[{'google_search_retrieval': {'dynamic_retrieval_config': {'dynamic_threshold': 0.3}}}]
                )
                response = model.generate_content(f"Найди 50 видео и проанализируй: {data}")
            except Exception:
                # ПОПЫТКА 3: Строковый формат (самый простой)
                model = genai.GenerativeModel(model_name=selected_model, tools=['google_search_retrieval'])
                response = model.generate_content(f"Найди 50 видео и проанализируй: {data}")

        return response.text

    except Exception as e:
        return f"Критическая ошибка (Grounding Fail): {str(e)}. Пожалуйста, проверьте логи Render."