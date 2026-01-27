from pytrends.request import TrendReq
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_mock_data(keywords_list):
    """Генерирует красивые фейковые данные, если Google заблокировал"""
    print(f"⚠️ Google Blocked. Генерирую демо-данные для: {keywords_list}")
    mock_data = []
    
    # Генерируем данные за 12 месяцев
    current_date = datetime.now() - timedelta(days=365)
    
    for _ in range(12):
        item = {"date": current_date.strftime('%Y-%m')}
        
        # Для каждого слова придумываем случайное число (тренд)
        for key in keywords_list:
            # Случайное число от 10 до 100
            item[key] = random.randint(20, 100)
            
        mock_data.append(item)
        current_date += timedelta(days=30)
        
    return mock_data

def get_trends_data(keywords_list):
    print(f"📈 Запрашиваю Google Trends для: {keywords_list}")
    
    try:
        # Пытаемся подключиться (таймаут 5 секунд)
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(5,5))
        pytrends.build_payload(keywords_list, cat=0, timeframe='today 12-m', geo='', gprop='')
        
        data = pytrends.interest_over_time()
        
        if data.empty:
            raise Exception("Empty Data")

        chart_data = []
        for index, row in data.iterrows():
            item = {"date": index.strftime('%Y-%m-%d')}
            for keyword in keywords_list:
                item[keyword] = row[keyword]
            chart_data.append(item)
            
        print("✅ Данные от Google получены!")
        return chart_data

    except Exception as e:
        print(f"❌ Ошибка Google (включаю демо-режим): {e}")
        # Если ошибка — возвращаем фейковые данные, чтобы график работал
        return generate_mock_data(keywords_list)