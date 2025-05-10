import os
import requests

from dotenv import load_dotenv
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = os.getenv("API_URL")

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def generate_blog_post(prompt: str) -> str:
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.7,
        }
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    try:
        result = response.json()
        if isinstance(result, list):
            return result[0]["generated_text"]
        else:
            return f"Error: {result.get('error', 'Unknown error')}"
    except Exception as e:
        return f"Exception: {str(e)}"
