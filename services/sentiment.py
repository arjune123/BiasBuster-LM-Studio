from transformers import pipeline

def analyze_sentiment(articles):
    sentiment_analyzer = pipeline("sentiment-analysis")
    sentiments = []
    for article in articles:
        analysis = sentiment_analyzer(article['content'])[0]
        sentiments.append({
            "source": article['source'],
            "title": article['title'],
            "sentiment": analysis['label'],
            "score": analysis['score']
        })
    return sentiments