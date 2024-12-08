import requests
from datetime import datetime, timedelta
import config

def fetch_articles(category):
    base_url = "https://newsapi.org/v2/everything"
    
    # Get articles from the last 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    params = {
        'q': category,
        'from': start_date.strftime('%Y-%m-%d'),
        'to': end_date.strftime('%Y-%m-%d'),
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 10,
        'apiKey': config.NEWS_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        all_articles = response.json()['articles']
        valid_articles = []
        
        for article in all_articles:
            content = article.get('content') or article.get('description')
            if (content and 
                content.lower() != 'removed' and 
                '[removed]' not in content.lower() and
                len(content.strip()) > 50):
                valid_articles.append({
                    'source': article['source']['name'],
                    'title': article['title'],
                    'content': content,
                    'url': article['url']
                })
            
            if len(valid_articles) >= 3:
                break
                
        return valid_articles[:3]
        
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []