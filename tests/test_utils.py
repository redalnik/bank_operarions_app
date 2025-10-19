from unittest.mock import patch

from freezegun import freeze_time

from src.utils import cards, currencies, day_time, stock_prices, top_transactions


@freeze_time("2025-04-01 16:00:00")
def test_day_time_1():
    created_at = "Добрый день"
    assert created_at == day_time()


@freeze_time("2025-04-01 07:00:00")
def test_day_time_2():
    created_at = "Доброе утро"
    assert created_at == day_time()


@freeze_time("2025-04-01 01:00:00")
def test_day_time_3():
    created_at = "Доброй ночи"
    assert created_at == day_time()


@freeze_time("2025-04-01 20:00:00")
def test_day_time_4():
    created_at = "Добрый вечер"
    assert created_at == day_time()


def test_cards(sample_df):
    assert cards(sample_df) == [
        {"cashback": 2.0, "last_digits": "1111", "total_spent": 200},
        {"cashback": 3.0, "last_digits": "2222", "total_spent": 300},
        {"cashback": 4.0, "last_digits": "3333", "total_spent": 400},
        {"cashback": 5.0, "last_digits": "4444", "total_spent": 500},
        {"cashback": 1.0, "last_digits": "5091", "total_spent": 100},
        {"cashback": 6.0, "last_digits": "5555", "total_spent": 600},
        {"cashback": 7.0, "last_digits": "6666", "total_spent": 700},
        {"cashback": 8.0, "last_digits": "7777", "total_spent": 800},
        {"cashback": 9.0, "last_digits": "8888", "total_spent": 900},
    ]


def test_top_transactions(sample_df):
    assert top_transactions(sample_df) == [
        {"amount": 900, "category": "Супермаркеты", "date": "03.12.2024", "description": "FixPrice"},
        {"amount": 800, "category": "Супермаркеты", "date": "02.12.2024", "description": "Metro"},
        {"amount": 700, "category": "Кафе", "date": "01.12.2024", "description": "Кофейня"},
        {"amount": 600, "category": "Супермаркеты", "date": "03.11.2024", "description": "Ашан"},
        {"amount": 500, "category": "Кафе", "date": "02.11.2024", "description": "Шоколадница"},
    ]


def test_currencies():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"rates": {"USD": 0.023}}
        result = currencies("USD")
        assert result == [{"currency": "USD", "rate": 43.48}]


def test_stock_prices():
    with patch("finnhub.Client") as mock_client:
        # Создаем мок клиента
        mock_finnhub = mock_client.return_value

        # Настраиваем мок для ответов API
        mock_finnhub.quote.side_effect = [
            {"c": 150.25},  # AAPL цена
            {"c": 250.50}   # TSLA цена
        ]

        stocks = ["AAPL", "TSLA"]
        result = stock_prices(stocks)

        # Проверяем результат
        expected = [
            {"stock": "AAPL", "price": 150.25},
            {"stock": "TSLA", "price": 250.50}
        ]
        assert result == expected

        # Проверяем, что клиент был создан с правильным API ключом
        mock_client.assert_called_once()

        # Проверяем, что quote был вызван для каждой акции
        assert mock_finnhub.quote.call_count == 2
        mock_finnhub.quote.assert_any_call("AAPL")
        mock_finnhub.quote.assert_any_call("TSLA")
