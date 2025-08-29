import os
from datetime import datetime
from pricewatcher.scraper import fetch_product_page, parse_price
from pricewatcher.storage import read_yaml, read_json, write_json

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(
    BASE_DIR, '../config/products.yaml'))
DATA_FOLDER = os.path.abspath(os.path.join(BASE_DIR, '../data'))
HISTORY_PATH = os.path.join(DATA_FOLDER, 'prices.json')


def track_prices():
    """Fetch current prices for all products and update price history."""
    products = read_yaml(CONFIG_PATH)
    history = read_json(HISTORY_PATH)
    today = datetime.now().strftime('%Y-%m-%d')

    for product in products:
        try:
            html = fetch_product_page(product['url'])
        except Exception as e:
            print(f"Error fetching page for {product['name']}: {e}")
            continue

        try:
            price = parse_price(html)
        except Exception as e:
            print(f"Error parsing price for {product['name']}: {e}")
            continue  # Skip adding this product to history

        if product['name'] not in history:
            history[product['name']] = []

        # Append today's price
        history[product['name']].append({
            'date': today,
            'price': price
        })

        print(f"{product['name']}: ${price:.2f}")

    write_json(HISTORY_PATH, history)


if __name__ == "__main__":
    track_prices()
