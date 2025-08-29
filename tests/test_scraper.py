from pricewatcher.scraper import fetch_product_page, parse_price
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../pricewatcher')))


PRODUCT = {
    "name": "Gyeon Wetcoat Sealant 500mL",
    "url": "https://www.supercheapauto.com.au/p/gyeon-gyeon-wetcoat-sealant-500ml/707086.html"
}


def test_fetch_product_page_success():
    html = fetch_product_page(PRODUCT["url"])
    assert html is not None
    assert "<html" in html.lower()


def test_fetch_product_page_invalid_url():
    with pytest.raises(Exception):
        fetch_product_page("https://invalid-url.test/product")


def test_parse_price_success():
    html = fetch_product_page(PRODUCT["url"])
    price = parse_price(html)
    assert isinstance(price, float)
    assert price > 0


def test_parse_price_missing():
    html = "<html><body>No price here</body></html>"
    with pytest.raises(ValueError):
        parse_price(html)
