import datetime
import logging
import os

import finnhub  # type: ignore
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def day_time() -> str:
    """
    Возвращает приветствие в зависимости от текущего времени суток.
    """
    now_time = datetime.datetime.now().hour

    if 18 <= now_time <= 21:
        result = "Добрый вечер"
    elif 6 <= now_time <= 10:
        result = "Доброе утро"
    elif 11 <= now_time <= 17:
        result = "Добрый день"
    else:
        result = "Доброй ночи"
    logging.info("Определено приветствие по времени суток")
    return result


def cards(df: pd.DataFrame) -> list[dict]:
    """
    Собирает агрегированную статистику по картам: последние цифры, сумма трат, кэшбэк.
    """
    filtered_df = df[df["Сумма платежа"] < 0]
    grouped_df = filtered_df.groupby("Номер карты")
    result_df = grouped_df["Сумма платежа"].sum().abs()
    cards_dict = result_df.to_dict()
    cards_list = []
    for card_number, amount in cards_dict.items():
        cards_list.append({
            "last_digits": card_number[-4:],
            "total_spent": round(amount, 2),
            "cashback": round(amount / 100, 2),
        })
    logging.info("Сводная статистика по картам сформирована")
    return cards_list


def top_transactions(df: pd.DataFrame) -> list[dict]:
    """
    Возвращает топ-5 транзакций по абсолютной сумме списаний.
    """
    df_sorted = df.sort_values("Сумма платежа")
    df_top = df_sorted[:5].to_dict(orient="records")
    top_list = []
    for transaction in df_top:
        top_list.append(
            {
                "date": transaction["Дата платежа"],
                "amount": abs(transaction["Сумма платежа"]),
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )
    logging.info("Топ-5 транзакций определён")
    return top_list


def currencies(symbols: str) -> list[dict]:
    """
    Возвращает курсы указанных валют к рублю.
    """
    base = "RUB"
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"

    headers = {"apikey": os.getenv("APILAYER_KEY")}

    result_currencies: list[dict] = []
    try:
        response = requests.get(url, headers=headers, data={}, timeout=10)
        response.raise_for_status()
        data = response.json() or {}
        rates = data.get("rates", {}) or {}
        for currency, rate in rates.items():
            if not rate:
                continue
            result_currencies.append({
                "currency": currency,
                "rate": round(1 / rate, 2),
            })
        logging.info(f"Получены курсы валют для: {symbols}")
    except requests.RequestException as exc:
        logging.error(f"Ошибка при запросе курсов валют: {exc}")
    return result_currencies


def stock_prices(stocks: list[str]) -> list[dict]:
    """
    Возвращает текущие цены акций по тикерам.
    """
    finnhub_client = finnhub.Client(api_key=os.getenv("APIFINN"))

    result_stocks: list[dict] = []
    for stock_symbol in stocks:
        try:
            quote = finnhub_client.quote(stock_symbol)
            price = quote.get("c") if isinstance(quote, dict) else None
            if price is None:
                continue
            result_stocks.append({"stock": stock_symbol, "price": price})
        except Exception as exc:
            logging.error(f"Ошибка при запросе котировок для {stock_symbol}: {exc}")
            continue
    logging.info(f"Получены котировки акций: {stocks}")

    return result_stocks
