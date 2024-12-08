import requests
import config

def summarize_articles(articles):
    prompt = """There are multiple news articles about similar topic.
    Analyze them and provide a neutral, balanced summary that includes all perspectives. Focus on the facts.
    Provide a critical summary of the articles.It can be sufficiently long but not very long.

    Articles:
    """ + "\n\n".join([f"Source: {article['source']}\nTitle: {article['title']}\nContent: {article['content']}" 
                       for article in articles])
    
    url = f"{config.LM_STUDIO_API_URL}/v1/chat/completions"  # Make sure this matches
    
    payload = {
        "messages": [
            {"role": "system", "content": "You are a neutral news analyzer that provides balanced summaries."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "model": "llama-3.2-3b-qnn",
        "stream": False
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "Failed to generate summary. Please try again."
    except Exception as e:
        return f"Error generating summary: {str(e)}"