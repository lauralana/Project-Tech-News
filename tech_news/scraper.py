import time
import requests
from parsel import Selector
import re
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, {"user-agent": "Fake user-agent"},
                                timeout=3)
        if response.status_code == 200:
            return response.text
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)
    return selector.css('.cs-overlay-link::attr(href)').getall()


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    return selector.css('.next::attr(href)').get()


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)
    # regex = re.compile(r"<[^>]+>")

    url = selector.css('link[rel=canonical]::attr(href)').get()
    title = selector.css('.entry-title::text').get().strip('\xa0')
    timestamp = selector.css('.meta-date::text').get()
    writer = selector.css('.author a::text').get()
    reading_time = int(selector.css(
        '.meta-reading-time::text').get().split(' ')[0])
    summary = selector.css('.entry-content p').get()
    summary = re.sub('<.*?>', '', summary).strip()
    category = selector.css('.label::text').get()
    return {
        'url': url,
        'title': title,
        'timestamp': timestamp,
        'writer': writer,
        'reading_time': reading_time,
        'summary': summary,
        'category': category
    }


# Requisito 5
def get_tech_news(amount):
    list_news = []
    url = 'https://blog.betrybe.com/'
    while len(list_news) < amount:
        response = fetch(url)
        updates = scrape_updates(response)
        list_news.extend(updates)
        url = scrape_next_page_link(response)
    arr_list_news = []
    for item in list_news[:amount]:
        scrap_news = scrape_news(fetch(item))
        arr_list_news.append(scrap_news)
    create_news(arr_list_news)
    return arr_list_news[:amount]
    # agredecimentos a Ray Santiago e Dan Rubens por iluminar minha mente
    # #GRATILUZ
