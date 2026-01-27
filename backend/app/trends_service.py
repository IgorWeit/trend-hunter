from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime, timedelta

# Фейковая функция удалена. Только правда.

def get_trends_data(keywords_list):
    print(f"📈 Запрашиваю Google Trends для: {keywords_list}")
    
    try:
        # Увеличил таймаут до 10-25 секунд, чтобы Google реже отваливался
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25))
        pytrends.build_payload(keywords_list, cat=0, timeframe='today 12-m', geo='', gprop='')
        
        data = pytrends.interest_over_time()
        
        if data.empty:
            # Если данных нет — честно говорим об этом
            raise Exception("Google вернул 0 результатов. Попробуйте изменить запрос.")

        chart_data = []
        for index, row in data.iterrows():
            item = {"date": index.strftime('%Y-%m-%d')}
            for keyword in keywords_list:
                # Если вдруг Google вернул данные, но без нужной колонки
                if keyword in row:
                    item[keyword] = row[keyword]
                else:
                    item[keyword] = 0
            chart_data.append(item)
            
        print("✅ Данные от Google получены!")
        return chart_data

    except Exception as e:
        print(f"❌ Ошибка Google: {e}")
        # ВАЖНО: Мы больше не скрываем ошибку. Мы кидаем её в лицо Фронтенду.
        # Теперь сайт покажет Alert с текстом ошибки, а не фейковый график.
        raise Exception(f"Не удалось получить данные: {str(e)}")
