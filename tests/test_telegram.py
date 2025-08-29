import os
import requests

# Make sure your .env is loaded if you use python-dotenv
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        print("Message sent successfully!")
    except Exception as e:
        print(f"Failed to send message: {e}")


# Test sending a message
send_telegram("🚀 Test message from local machine")
