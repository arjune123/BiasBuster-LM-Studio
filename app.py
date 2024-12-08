from flask import Flask, request, jsonify, render_template
from services.lm_studio import summarize_articles
from services.news_fetcher import fetch_articles
from services.sentiment import analyze_sentiment
from services.summarizer import create_news_digest

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch_news():
    data = request.get_json()
    category = data['category']
    timeframe = data.get('timeframe', '7')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    article_count = data.get('article_count', '3')
    
    articles = fetch_articles(
        category, 
        timeframe=timeframe,
        start_date=start_date,
        end_date=end_date,
        article_count=int(article_count)
    )
    return jsonify(articles)

@app.route('/fetch-urls', methods=['POST'])
def fetch_from_url():
    data = request.get_json()
    urls = data.get('urls', [])
    
    if not urls:
        return jsonify([])
    
    articles = [
        {
            'source': f"Article {i+1}",
            'title': f"Article from {url}",
            'content': url,
            'url': url
        }
        for i, url in enumerate(urls)
    ]
    
    return jsonify(articles)

@app.route('/analyze', methods=['POST'])
def analyze_news():
    articles = request.json['articles']
    analysis = analyze_sentiment(articles)
    summary = summarize_articles(articles)
    return jsonify({'analysis': analysis, 'summary': summary})

@app.route('/digest', methods=['POST'])
def create_digest():
    articles = request.json['articles']
    digest = create_news_digest(articles)
    return jsonify({'digest': digest})

if __name__ == '__main__':
    app.run(debug=True)
