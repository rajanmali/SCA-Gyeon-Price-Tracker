import os
import json
import yaml
from datetime import datetime
from pricewatcher.scraper import fetch_product_page, parse_price

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(
    BASE_DIR, '../config/products.yaml'))
DATA_FOLDER = os.path.abspath(os.path.join(BASE_DIR, '../data'))
HISTORY_PATH = os.path.join(DATA_FOLDER, 'prices.json')

# Ensure data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)


def load_products():
    """Load products from YAML config file."""
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)


def load_history():
    """Load price history from JSON file."""
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, 'r') as f:
            return json.load(f)
    return {}


def save_history(history):
    """Save price history to JSON file."""
    with open(HISTORY_PATH, 'w') as f:
        json.dump(history, f, indent=2)


def track_prices():
    """Fetch current prices for all products and update price history."""
    products = load_products()
    history = load_history()
    today = datetime.now().strftime('%Y-%m-%d')

    for product in products:
        try:
            html = fetch_product_page(product['url'])
            price = parse_price(html)
        except Exception as e:
            print(f"Error fetching price for {product['name']}: {e}")
            continue

        if product['name'] not in history:
            history[product['name']] = []

        # Append today's price
        history[product['name']].append({
            'date': today,
            'price': price
        })

        print(f"{product['name']}: ${price:.2f}")

    save_history(history)


if __name__ == "__main__":
    track_prices()
