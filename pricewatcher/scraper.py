# pricewatcher/scraper.py

import requests
from bs4 import BeautifulSoup


def fetch_product_page(url: str) -> str:
    """
    Fetches the HTML content of a product page.

    Args:
        url (str): URL of the product page.

    Returns:
        str: HTML content.

    Raises:
        Exception: If request fails or status code != 200.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch page: {url}, Status code: {response.status_code}")
        return response.text
    except requests.RequestException as e:
        raise Exception(f"Error fetching page: {url}") from e


def parse_price(html: str) -> float:
    """
    Parses the price from a Supercheap Auto product page HTML.

    Args:
        html (str): HTML content of product page.

    Returns:
        float: Price of the product.

    Raises:
        ValueError: If price cannot be found or parsed.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Supercheap Auto uses <span class="price">PRICE</span>
    price_tag = soup.find("span", class_="price")

    if not price_tag or not price_tag.text:
        raise ValueError("Price not found on page")

    # Remove $ and commas, convert to float
    price_str = price_tag.text.replace("$", "").replace(",", "").strip()

    try:
        return float(price_str)
    except ValueError:
        raise ValueError(f"Unable to parse price: {price_str}")
