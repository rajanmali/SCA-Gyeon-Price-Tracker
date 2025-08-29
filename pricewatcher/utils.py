# pricewatcher/utils.py
from typing import List, Dict


def has_price_dropped(history: Dict[str, List[Dict]], product_name: str, new_price: float) -> bool:
    """Check if the price has dropped compared to the latest recorded price."""
    if product_name not in history or not history[product_name]:
        return False
    last_price = history[product_name][-1]["price"]
    return new_price < last_price


def has_price_increased(history: Dict[str, List[Dict]], product_name: str, new_price: float) -> bool:
    """Check if the price has increased compared to the latest recorded price."""
    if product_name not in history or not history[product_name]:
        return False
    last_price = history[product_name][-1]["price"]
    return new_price > last_price


def format_price_message(product_name: str, old_price: float, new_price: float) -> str:
    """
    Format a Telegram message for a price change.

    Args:
        product_name (str): Name of the product.
        old_price (float): Previous price.
        new_price (float): Current price.

    Returns:
        str: Formatted message.
    """
    if new_price < old_price:
        emoji = "📉"
        change_type = "Price drop alert!"
    elif new_price > old_price:
        emoji = "📈"
        change_type = "Price increase alert!"
    else:
        emoji = "ℹ️"
        change_type = "Price unchanged"

    return f"{emoji} {change_type}\n{product_name} is now ${new_price:.2f} (was ${old_price:.2f})"
