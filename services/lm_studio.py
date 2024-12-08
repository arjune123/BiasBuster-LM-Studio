import requests
import config

def summarize_articles(articles):
    url = f"{config.LM_STUDIO_API_URL}/summarize"
    payload = {"articles": articles}
    headers = {"Authorization": f"Bearer {config.LM_STUDIO_API_KEY}"}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()['summary']
    else:
        raise Exception(f"Failed to summarize articles: {response.status_code} {response.text}")