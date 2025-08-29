import os
from datetime import datetime
from pricewatcher.scraper import fetch_product_page, parse_price
from pricewatcher.storage import read_yaml, read_json, write_json
from pricewatcher.notifier import send_telegram
from pricewatcher.config import PRODUCTS_YAML, PRICES_JSON


def track_prices():
    """Fetch current prices for all products, update history, and send notifications."""

    # Send confirmation that script has started
    send_telegram(
        f"🟢 Price tracker started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    products = read_yaml(PRODUCTS_YAML)
    history = read_json(PRICES_JSON)
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

        # Optional: detect price drop
        last_price = history[product['name']
                             ][-1]['price'] if history[product['name']] else None
        if last_price is not None and price < last_price:
            send_telegram(
                f"📉 Price dropped for {product['name']}! ${last_price:.2f} → ${price:.2f}")

        # Append today's price
        history[product['name']].append({
            'date': today,
            'price': price
        })

        print(f"{product['name']}: ${price:.2f}")

    write_json(PRICES_JSON, history)


if __name__ == "__main__":
    track_prices()
