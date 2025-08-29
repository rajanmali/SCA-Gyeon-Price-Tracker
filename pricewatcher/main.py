import os
from datetime import datetime
from pricewatcher.scraper import fetch_product_page, parse_price
from pricewatcher.storage import read_yaml, read_json, write_json
from pricewatcher.notifier import send_telegram
from pricewatcher.utils import has_price_dropped
from pricewatcher.config import PRODUCTS_YAML, PRICES_JSON


def track_prices():
    """Fetch current prices for all products, update history, and notify on price drops."""
    products = read_yaml(PRODUCTS_YAML)
    history = read_json(PRICES_JSON)
    today = datetime.now().strftime('%Y-%m-%d')

    for product in products:
        product_name = product['name']

        # Fetch product page
        try:
            html = fetch_product_page(product['url'])
        except Exception as e:
            print(f"Error fetching page for {product_name}: {e}")
            continue

        # Parse price
        try:
            price = parse_price(html)
        except Exception as e:
            print(f"Error parsing price for {product_name}: {e}")
            continue

        # Initialize history if missing
        if product_name not in history:
            history[product_name] = []

        # Check for price drop
        if has_price_dropped(history, product_name, price):
            last_price = history[product_name][-1]['price']
            message = f"📉 Price drop alert!\n{product_name} is now ${price:.2f} (was ${last_price:.2f})"
            send_telegram(message)

        # Append today's price
        history[product_name].append({
            'date': today,
            'price': price
        })

        print(f"{product_name}: ${price:.2f}")

    # Save updated history
    write_json(PRICES_JSON, history)


if __name__ == "__main__":
    track_prices()
