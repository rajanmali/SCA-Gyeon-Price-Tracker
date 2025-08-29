# pricewatcher/utils.py
from typing import List, Dict


def has_price_dropped(history: Dict[str, List[Dict]], product_name: str, new_price: float) -> bool:
    """
    Check if the price of a product has dropped compared to the latest recorded price.

    Args:
        history (dict): Price history dictionary.
        product_name (str): Name of the product.
        new_price (float): Latest price of the product.

    Returns:
        bool: True if price has dropped, False otherwise.
    """
    if product_name not in history or not history[product_name]:
        return False  # No previous price to compare

    last_price = history[product_name][-1]["price"]
    return new_price < last_price
