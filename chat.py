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

def query(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def format_history(chat_history):
    # Build a prompt that includes the entire chat history
    prompt = ""
    for pair in chat_history:
        prompt += f"User: {pair['user']}\nAssistant: {pair['assistant']}\n"
    return prompt

if __name__ == "__main__":
    chat_history = []

    print("💬 Start chatting with the AI (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Add the new user input to the chat history, with an empty assistant response
        chat_history.append({"user": user_input, "assistant": ""})
        
        # Build the full prompt
        full_prompt = format_history(chat_history[:-1]) + f"User: {user_input}\nAssistant:"
        
        response = query(full_prompt)

        if isinstance(response, list) and 'generated_text' in response[0]:
            full_response = response[0]['generated_text']
            # Extract only the assistant's new reply
            assistant_reply = full_response.replace(full_prompt, "").strip()
            chat_history[-1]['assistant'] = assistant_reply
            print(f"AI: {assistant_reply}\n")
        else:
            print("⚠️ Error: Unexpected response format or empty response.")
