import requests
import json
import config

def analyze_sentiment(articles):
    sentiments = []
    
    for article in articles:
        prompt = f"""Analyze the sentiment and political bias of this news article. 
        If you cannot access or analyze the article, respond with a JSON error format.
        
        Article from {article['source']}:
        URL: {article['content']}
        
        Respond in one of these formats:
        Success: {{"sentiment": "POSITIVE/NEGATIVE/NEUTRAL", "score": 0.0-1.0}}
        Error: {{"error": true, "message": "reason for failure"}}
        """

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a sentiment analyzer. Always respond with valid JSON."
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
                    
                    # Extract JSON from markdown if present
                    if "```" in content:
                        json_str = content.split("```")[1].strip()
                        if json_str.startswith('json'):
                            json_str = json_str[4:].strip()
                    else:
                        # Find JSON object in the content
                        start = content.find('{')
                        end = content.rfind('}') + 1
                        if start >= 0 and end > start:
                            json_str = content[start:end]
                        else:
                            raise Exception("No JSON found in response")
                    
                    analysis = json.loads(json_str)
                    
                    if 'error' in analysis:
                        sentiments.append({
                            "source": article['source'],
                            "title": article['title'],
                            "sentiment": "ERROR",
                            "score": 0,
                            "error_message": analysis['message']
                        })
                    else:
                        sentiments.append({
                            "source": article['source'],
                            "title": article['title'],
                            "sentiment": analysis['sentiment'],
                            "score": analysis['score']
                        })
            else:
                raise Exception(f"API Error: {response.status_code}")
                
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            sentiments.append({
                "source": article['source'],
                "title": article['title'],
                "sentiment": "ERROR",
                "score": 0,
                "error_message": str(e)
            })
    
    return sentiments