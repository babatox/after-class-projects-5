import requests
from config import HF_API_KEY

def classify_text(text):
    url = "https://router.huggingface.co/hf-inference/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": text}
    response = requests.post(url, headers=headers, json=payload)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
       print(f"Requests failed with status code {response.status_code}")
       print(f"Response text: {response.text}")
       return{}
    
if __name__ == "__main__":
    sample_text = "I love using Hugging Face APIs!"
    result = classify_text(sample_text)
    print(result)