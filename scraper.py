# scraper.py
import feedparser
import re

def clean_html(raw_html):
    return re.sub(r'<[^>]+>', '', raw_html)

def get_news():
    from config import RSS_FEEDS
    articles = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:20]:  # últimas 5 noticias
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'summary': clean_html(entry.summary),
                'published': entry.get('published', 'Fecha desconocida')
            })
    return articles
