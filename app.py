from flask import Flask, request, jsonify, render_template
from services.lm_studio import summarize_articles
from services.news_fetcher import fetch_articles
from services.sentiment import analyze_sentiment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch_news():
    category = request.form['category']
    articles = fetch_articles(category)
    return jsonify(articles)

@app.route('/analyze', methods=['POST'])
def analyze_news():
    articles = request.json['articles']
    analysis = analyze_sentiment(articles)
    summary = summarize_articles(articles)
    return jsonify({'analysis': analysis, 'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
