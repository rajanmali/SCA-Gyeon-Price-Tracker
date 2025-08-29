import pytest
from unittest.mock import patch
from pricewatcher.main import track_prices

# Sample product list
sample_products = [
    {"name": "Product 1", "url": "https://example.com/1"},
    {"name": "Product 2", "url": "https://example.com/2"},
]


@patch("pricewatcher.main.read_yaml")
@patch("pricewatcher.main.read_json")
@patch("pricewatcher.main.write_json")
@patch("pricewatcher.main.fetch_product_page")
@patch("pricewatcher.main.parse_price")
def test_track_prices_success(mock_parse_price, mock_fetch, mock_write_json, mock_read_json, mock_read_yaml):
    # Normal successful run
    mock_read_yaml.return_value = sample_products
    mock_read_json.return_value = {}

    mock_fetch.side_effect = lambda url: "<html></html>"
    mock_parse_price.side_effect = [19.99, 29.99]

    track_prices()

    # Check correct calls
    assert mock_fetch.call_count == 2
    assert mock_parse_price.call_count == 2
    assert mock_write_json.call_count == 1
    written_data = mock_write_json.call_args[0][1]
    assert "Product 1" in written_data and "Product 2" in written_data


@patch("pricewatcher.main.read_yaml")
@patch("pricewatcher.main.read_json")
@patch("pricewatcher.main.write_json")
@patch("pricewatcher.main.fetch_product_page")
@patch("pricewatcher.main.parse_price")
def test_track_prices_fetch_error(mock_parse_price, mock_fetch, mock_write_json, mock_read_json, mock_read_yaml):
    mock_read_yaml.return_value = sample_products
    mock_read_json.return_value = {}

    # Simulate fetch error for Product 1
    def fetch_side_effect(url):
        if "1" in url:
            raise Exception("Network error")
        return "<html></html>"
    mock_fetch.side_effect = fetch_side_effect
    mock_parse_price.side_effect = [29.99]  # Only called for Product 2

    track_prices()

    # Check fetch and parse calls
    assert mock_fetch.call_count == 2
    assert mock_parse_price.call_count == 1  # Only Product 2 parsed
    written_data = mock_write_json.call_args[0][1]
    assert "Product 1" not in written_data or len(
        written_data["Product 1"]) == 0
    assert "Product 2" in written_data


@patch("pricewatcher.main.read_yaml")
@patch("pricewatcher.main.read_json")
@patch("pricewatcher.main.write_json")
@patch("pricewatcher.main.fetch_product_page")
@patch("pricewatcher.main.parse_price")
def test_track_prices_parse_error(mock_parse_price, mock_fetch, mock_write_json, mock_read_json, mock_read_yaml):
    mock_read_yaml.return_value = sample_products
    mock_read_json.return_value = {}

    mock_fetch.side_effect = lambda url: "<html></html>"
    # Simulate parse error for Product 1

    def parse_side_effect(html):
        if "1" in html:
            raise ValueError("Price not found")
        return 29.99
    mock_parse_price.side_effect = parse_side_effect

    track_prices()

    assert mock_fetch.call_count == 2
    assert mock_parse_price.call_count == 2
    written_data = mock_write_json.call_args[0][1]
    assert "Product 1" not in written_data or len(
        written_data["Product 1"]) == 0
    assert "Product 2" in written_data


@patch("pricewatcher.main.read_yaml")
@patch("pricewatcher.main.read_json")
@patch("pricewatcher.main.write_json")
@patch("pricewatcher.main.fetch_product_page")
@patch("pricewatcher.main.parse_price")
def test_track_prices_existing_history(mock_parse_price, mock_fetch, mock_write_json, mock_read_json, mock_read_yaml):
    mock_read_yaml.return_value = sample_products
    # Existing history
    mock_read_json.return_value = {
        "Product 1": [{"date": "2025-08-28", "price": 18.99}]
    }

    mock_fetch.side_effect = lambda url: "<html></html>"
    mock_parse_price.side_effect = [19.99, 29.99]

    track_prices()

    written_data = mock_write_json.call_args[0][1]
    # Check that new price is appended, not overwriting
    assert len(written_data["Product 1"]) == 2
    assert written_data["Product 1"][-1]["price"] == 19.99
    assert "Product 2" in written_data
