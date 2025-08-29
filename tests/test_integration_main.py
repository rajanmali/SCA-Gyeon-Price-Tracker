# tests/test_integration_main.py
import pytest
from unittest.mock import patch
from pricewatcher.main import track_prices

# Sample product list for testing
sample_products = [
    {"name": "Product A", "url": "https://example.com/a"},
    {"name": "Product B", "url": "https://example.com/b"},
]

# Helper for creating fake HTML responses


def fake_html(url):
    return "<html></html>"


@pytest.mark.parametrize("history,expected_notifications", [
    # Case 1: Both products have new prices, first entry -> no notifications
    ({}, 0),
    # Case 2: Product A drops, Product B increases -> 2 notifications
    ({"Product A": [{"date": "2025-08-28", "price": 20.0}],
      "Product B": [{"date": "2025-08-28", "price": 25.0}]}, 2),
])
@patch("pricewatcher.main.read_yaml")
@patch("pricewatcher.main.read_json")
@patch("pricewatcher.main.write_json")
@patch("pricewatcher.main.fetch_product_page")
@patch("pricewatcher.main.send_telegram")
def test_notifications(mock_send, mock_fetch, mock_write_json, mock_read_json, mock_read_yaml, history, expected_notifications):
    mock_read_yaml.return_value = sample_products
    mock_read_json.return_value = history
    mock_fetch.side_effect = lambda url: fake_html(url)

    # Simulate parse_price returning different values for each product
    def parse_side_effect(html):
        if "a" in html:
            return 19.0  # Product A drops
        return 26.0      # Product B increases

    with patch("pricewatcher.main.parse_price", side_effect=parse_side_effect):
        track_prices()

    assert mock_send.call_count == expected_notifications
