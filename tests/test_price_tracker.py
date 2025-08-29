import pytest
from unittest.mock import patch, MagicMock
from pricewatcher.main import track_prices
from pricewatcher.scraper import fetch_product_page, parse_price

# Sample product list to return from YAML
sample_products = [
    {"name": "Product 1", "url": "https://example.com/1"},
    {"name": "Product 2", "url": "https://example.com/2"},
]

# Sample prices to return from parse_price
sample_prices = [19.99, 29.99]


@patch("pricewatcher.main.read_yaml")
@patch("pricewatcher.main.read_json")
@patch("pricewatcher.main.write_json")
@patch("pricewatcher.main.fetch_product_page")
@patch("pricewatcher.main.parse_price")
def test_track_prices(mock_parse_price, mock_fetch, mock_write_json, mock_read_json, mock_read_yaml):
    # Mock YAML and JSON loading
    mock_read_yaml.return_value = sample_products
    mock_read_json.return_value = {}

    # Mock fetch and parse
    mock_fetch.side_effect = lambda url: "<html></html>"
    mock_parse_price.side_effect = sample_prices

    # Run the tracker
    track_prices()

    # Check YAML was loaded
    mock_read_yaml.assert_called_once()

    # Check each product was fetched and parsed
    assert mock_fetch.call_count == len(sample_products)
    assert mock_parse_price.call_count == len(sample_products)

    # Check JSON write called once
    mock_write_json.assert_called_once()
    # Check that prices were written correctly
    written_data = mock_write_json.call_args[0][1]
    assert "Product 1" in written_data
    assert "Product 2" in written_data
    assert written_data["Product 1"][0]["price"] == 19.99
    assert written_data["Product 2"][0]["price"] == 29.99
