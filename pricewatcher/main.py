# pricewatcher/main.py
import os
from datetime import datetime
from pricewatcher.scraper import fetch_product_page, parse_price
from pricewatcher.storage import read_yaml, read_json, write_json
from pricewatcher.notifier import send_telegram
from pricewatcher.config import PRODUCTS_YAML, PRICES_JSON
from pricewatcher.utils import has_price_dropped, has_price_increased, format_price_message


def track_prices():
    """Fetch current prices for all products, update history, and send notifications for changes."""
    products = read_yaml(PRODUCTS_YAML)
    history = read_json(PRICES_JSON)
    today = datetime.now().strftime('%Y-%m-%d')

    for product in products:
        product_name = product["name"]
        try:
            html = fetch_product_page(product["url"])
        except Exception as e:
            print(f"Error fetching page for {product_name}: {e}")
            continue

        try:
            price = parse_price(html)
        except Exception as e:
            print(f"Error parsing price for {product_name}: {e}")
            continue

        if product_name not in history:
            history[product_name] = []

        # Check price changes
        if history[product_name]:
            last_price = history[product_name][-1]["price"]
            if has_price_dropped(history, product_name, price) or has_price_increased(history, product_name, price):
                message = format_price_message(product_name, last_price, price)
                send_telegram(message)

        # Append today's price
        history[product_name].append({
            "date": today,
            "price": price
        })

        print(f"{product_name}: ${price:.2f}")

    write_json(PRICES_JSON, history)


if __name__ == "__main__":
    track_prices()
