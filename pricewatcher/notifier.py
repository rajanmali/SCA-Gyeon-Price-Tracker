# pricewatcher/notifier.py
import requests
from pricewatcher.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_telegram(message: str) -> bool:
    """
    Send a message via Telegram Bot.

    Args:
        message (str): The message to send.

    Returns:
        bool: True if message sent successfully, False otherwise.
    """
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"  # optional: allows bold, italics, etc.
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Failed to send Telegram message: {e}")
        return False
