import requests
import json
import config

def analyze_sentiment(articles):
    sentiments = []
    
    for article in articles:
        prompt = f"""Analyze the sentiment and political bias of this news article. 
        Provide the analysis as JSON with fields: sentiment (POSITIVE/NEGATIVE/NEUTRAL) and score (0-1).
        
        Article from {article['source']}:
        Title: {article['title']}
        Content: {article['content']}
        """

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a sentiment analyzer. Respond only with JSON in the format: {\"sentiment\": \"POSITIVE/NEGATIVE/NEUTRAL\", \"score\": 0.0-1.0}"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "model": "llama-3.2-3b-qnn",
            "stream": False
        }

        try:
            response = requests.post(
                f"{config.LM_STUDIO_API_URL}/v1/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    # Extract JSON from the content
                    if "```" in content:
                        json_str = content.split("```")[1].strip()
                        if json_str.startswith('json'):
                            json_str = json_str[4:].strip()
                    else:
                        json_str = content
                    analysis = json.loads(json_str)
                    sentiments.append({
                        "source": article['source'],
                        "title": article['title'],
                        "sentiment": analysis['sentiment'],
                        "score": analysis['score']
                    })
                else:
                    raise Exception("Invalid response format")
            else:
                raise Exception(f"API Error: {response.status_code}")
                
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            sentiments.append({
                "source": article['source'],
                "title": article['title'],
                "sentiment": "ERROR",
                "score": 0
            })
    
    return sentiments