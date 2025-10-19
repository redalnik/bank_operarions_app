from datetime import datetime

import pandas as pd

from src.utils import cards, currencies, day_time, stock_prices, top_transactions


def get_views(df: pd.DataFrame, user_setting: dict, date_time: str) -> dict:
    """
    Основная функция: собирает все данные в итоговый JSON для страницы "Главная".

    Args:
        df: DataFrame с транзакциями
        user_setting: Словарь с настройками пользователя
        date_time: Дата и время в формате "YYYY-MM-DD HH:MM:SS"

    Returns:
        Словарь с данными для главной страницы
    """
    currency = ",".join(user_setting["user_currencies"])
    stocks = user_setting["user_stocks"]
    end_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    start_date = datetime.strftime(end_date, "%Y-%m-01")

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]

    return {
        "greeting": day_time(),
        "cards": cards(df),
        "top_transactions": top_transactions(df),
        "currency_rates": currencies(currency),
        "stock_prices": stock_prices(stocks),
    }
