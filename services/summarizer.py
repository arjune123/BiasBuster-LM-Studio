import requests
import config
import string

def is_english(text):
    # Count ASCII characters vs total characters
    ascii_chars = 0
    total_chars = 0
    
    for char in text:
        if char.isspace() or char in string.punctuation:
            continue
        total_chars += 1
        if ord(char) < 128:  # ASCII range
            ascii_chars += 1
    
    # Consider text English if at least 80% of characters are ASCII
    return total_chars == 0 or (ascii_chars / total_chars) >= 0.8

def create_news_digest(articles):
    # Filter for English-only articles
    english_articles = []
    for article in articles:
        title = article.get('title', '')
        content = article.get('content', '')
        
        if is_english(title) and is_english(content):
            english_articles.append(article)
        else:
            print(f"Skipping non-English article: {title[:30]}...")  # Only log title start

    if not english_articles:
        return "No English articles to summarize"

    formatted_articles = []
    for i, article in enumerate(english_articles, 1):
        formatted_article = f"""
ARTICLE {i}:
SOURCE: {article.get('source', 'Unknown')}
TITLE: {article.get('title', 'Untitled')}
CONTENT: {article.get('content', '').strip()}
"""
        formatted_articles.append(formatted_article)

    prompt = f"""You are a precise news analyst. Analyze these {len(english_articles)} articles and create a summary.

{'\n'.join(formatted_articles)}

You may include:
1. An overview
2. Key points from each article (use bullet points)
3. Any common themes across articles
The goal is to provide a concise summary of the articles in a way that informs the reader about the main topics and events.
It can be sufficiently long to be useful, but not excessively long.

Focus only on the actual content provided."""

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a precise news analyst. Summarize only what is in the provided articles. Keep responses clear and factual."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "model": "llama-3.2-3b-qnn",
        "stream": False,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(
            f"{config.LM_STUDIO_API_URL}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return "Failed to generate digest. Please try again."
    except Exception as e:
        return f"Error generating digest: {str(e)}" 

def format_digest_content(content):
    # Ensure consistent markdown formatting
    content = content.replace('**', '##')  # Convert bold to h2 headers
    content = content.replace('Key points:', '### Key points:')  # Make subsections h3
    return content 