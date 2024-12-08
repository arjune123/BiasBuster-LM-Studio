import requests
from datetime import datetime, timedelta
import config

def fetch_articles(category, timeframe=7, start_date=None, end_date=None, article_count=3):
    base_url = "https://newsapi.org/v2/everything"
    
    # Calculate dates
    end_date = end_date or datetime.now()
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start_date = end_date - timedelta(days=int(timeframe))
    
    params = {
        'q': category,
        'from': start_date.strftime('%Y-%m-%d'),
        'to': end_date.strftime('%Y-%m-%d'),
        'language': 'en',
        'sortBy': 'publishedAt',  # Changed to get latest articles
        'pageSize': int(article_count),
        'apiKey': config.NEWS_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        articles = response.json()['articles']
        return [{
            'source': article['source']['name'],
            'title': article['title'],
            'content': article.get('content') or article.get('description'),
            'url': article['url'],
            'publishedAt': article['publishedAt']
        } for article in articles if article.get('content') or article.get('description')]
        
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []