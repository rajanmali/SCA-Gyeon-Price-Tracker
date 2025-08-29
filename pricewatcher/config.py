# pricewatcher/config.py
import os
from dotenv import load_dotenv

# Load .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

# Telegram Bot configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# File paths
CONFIG_FOLDER = os.path.join(BASE_DIR, "config")
DATA_FOLDER = os.path.join(BASE_DIR, "data")

PRODUCTS_YAML = os.path.join(CONFIG_FOLDER, "products.yaml")
PRICES_JSON = os.path.join(DATA_FOLDER, "prices.json")

# Validate required environment variables
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env")
