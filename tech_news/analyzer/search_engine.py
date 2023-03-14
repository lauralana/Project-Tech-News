from tech_news.database import search_news
from datetime import datetime


# Requisito 7
def search_by_title(title):
    list = []
    for info in search_news({"title": {"$regex": title, "$options": "i"}}):
        list.append((info['title'], info['url']))
    return list


# Requisito 8
def search_by_date(date):
    try:
        list = []
        for info in search_news({"timestamp": datetime.fromisoformat(
                                date).strftime("%d/%m/%Y")}):
            list.append((info['title'], info['url']))
        return list
    except ValueError:
        raise ValueError('Data inválida')


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
