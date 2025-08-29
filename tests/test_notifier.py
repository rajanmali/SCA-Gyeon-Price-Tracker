# tests/test_notifier.py
import pytest
from unittest.mock import patch, MagicMock
from pricewatcher.notifier import send_telegram


@pytest.mark.parametrize("message", [
    "Test message",
    "Another message with *Markdown*"
])
@patch("pricewatcher.notifier.requests.post")
def test_send_telegram_success(mock_post, message):
    # Mock successful response
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    result = send_telegram(message)
    assert result is True
    mock_post.assert_called_once()
    payload = mock_post.call_args[1]['data']
    assert payload['text'] == message


@patch("pricewatcher.notifier.requests.post")
def test_send_telegram_failure(mock_post):
    # Mock failed response (raise exception)
    mock_post.side_effect = Exception("Network error")

    result = send_telegram("Test message")
    assert result is False
    mock_post.assert_called_once()
