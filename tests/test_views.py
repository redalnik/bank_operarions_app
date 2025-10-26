from unittest.mock import patch

from src.views import get_views


@patch("src.views.currencies")
@patch("src.views.stock_prices")
def test_main_view_output(mock_stocks, mock_currencies, sample_df, sample_user_settings):
    mock_stocks.return_value = [{"stock": "AAPL", "price": 150.0}, {"stock": "GOOGL", "price": 2500.0}]
    mock_currencies.return_value = [{"currency": "USD", "rate": 73.0}, {"currency": "EUR", "rate": 86.0}]

    result = get_views(sample_df, sample_user_settings, "2021-12-31 16:00:00")

    assert isinstance(result, dict)
    assert isinstance(result["greeting"], str)
    assert isinstance(result["cards"], list)
    assert isinstance(result["top_transactions"], list)
    assert result["currency_rates"] == mock_currencies.return_value
    assert result["stock_prices"] == mock_stocks.return_value
