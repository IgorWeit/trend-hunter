import scrapetube

def get_real_trends(category):
    print(f"🕵️‍♂️ Ищу реальные тренды для: {category}...")
    
    # Добавляем "shorts", чтобы искать короткие видео
    query = f"{category} shorts"
    
    try:
        # Получаем генератор видео (это работает мгновенно)
        videos = scrapetube.get_search(query)
        
        data_text = "Список популярных Shorts за сегодня:\n"
        count = 0
        
        for video in videos:
            if count >= 10:  # Берем только 10 штук
                break
                
            # Безопасно достаем заголовок
            try:
                title = video['title']['runs'][0]['text']
                
                # Достаем просмотры (иногда их нет в явном виде)
                views = "N/A"
                if 'viewCountText' in video:
                    if 'simpleText' in video['viewCountText']:
                        views = video['viewCountText']['simpleText']
                    else:
                        # Иногда YouTube отдает просмотры в другом формате
                        views = "Many views"
                
                data_text += f"- {title} ({views})\n"
                count += 1
            except:
                continue # Если одно видео сбойнуло, пропускаем

        if count == 0:
             return "Не нашел видео. Попробуй другую категорию."

        print("✅ Данные собраны через scrapetube!")
        return data_text

    except Exception as e:
        print(f"❌ Ошибка scrapetube: {e}")
        return f"Ошибка сбора данных: {str(e)}"