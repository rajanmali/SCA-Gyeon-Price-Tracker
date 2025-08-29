from pricewatcher.scraper import fetch_product_page, parse_price
import pytest
import sys
import os
import yaml

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../pricewatcher')))

# Load products from YAML
CONFIG_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../config/products.yaml'))
with open(CONFIG_PATH, 'r') as f:
    PRODUCTS = yaml.safe_load(f)


@pytest.mark.parametrize("product", PRODUCTS)
def test_fetch_product_page_success(product):
    html = fetch_product_page(product["url"])
    assert html is not None
    assert "<html" in html.lower()


@pytest.mark.parametrize("product", PRODUCTS)
def test_parse_price_success(product):
    html = fetch_product_page(product["url"])
    price = parse_price(html)
    assert isinstance(price, float)
    assert price > 0


def test_fetch_product_page_invalid_url():
    with pytest.raises(Exception):
        fetch_product_page("https://invalid-url.test/product")


def test_parse_price_missing():
    html = "<html><body>No price here</body></html>"
    with pytest.raises(ValueError):
        parse_price(html)
