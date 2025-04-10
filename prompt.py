from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
API_KEY = os.getenv("HUGGINGFACE_TOKEN")
# API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-V3-0324"
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if __name__ == "__main__":
    # Tell user to enter the prompt
    print("💬 Enter your prompt (type 'exit' to quit):")
    # print("💬 Enter your prompt (exi)")

    # Example usage
    prompt = input("You: ")
    if prompt.lower() in ["exit", "quit"]:
        exit(0)
    
    result = query({
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7,
            "top_p": 0.9
        }
    })
    # Remove the prompt from the result
    if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
        result[0]['generated_text'] = result[0]['generated_text'].replace(prompt, '')
    else:
        print("Error: Unexpected response format or empty response.")
        exit(1)
    
    print(result[0]['generated_text'])

