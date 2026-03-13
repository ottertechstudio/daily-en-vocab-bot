import os
import requests
 
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
 
def get_vocab():
    prompt = """
Create a daily English vocabulary lesson for learners.
Format exactly like this:


Word: [english word]
Meaning: [clear simple English meaning]
Spoken English: [how to use in spoken English + simple English explanation]
Written English: [how to use in written English + simple English explanation]
Examples:
1. [example sentence 1]
2. [example sentence 2]
3. [example sentence 3]
Watch Out: [common mistakes and tips in simple English]


Keep it beginner-friendly. Use simple and clear English only.
Do NOT use any other language. Everything must be in English only.
    """
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    if "choices" not in data:
        raise Exception(f"API Error: {data}")
    return data["choices"][0]["message"]["content"]
 
def send_vocab():
    vocab = get_vocab()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": vocab
    })
    print("Vocab sent!")
 
send_vocab()
