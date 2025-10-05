import json
import logging
import os
from datetime import datetime
import requests
import pandas as pd


from config import PATH_TO_OPERATIONS

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
url = "https://api.apilayer.com/exchangerates_data/convert"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Пример пользовательских настроек (обычно загружаются из user_settings.json)
USER_SETTINGS = {
    "user_currencies": ["USD", "EUR"],
    "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
}


def get_greeting(date_str: str) -> str:
    """Рассчитывает и выводит приветствие в зависимости от заданного времени."""
    date_now = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    if 6 <= date_now.hour < 12:
        return "Доброе утро"
    elif 12 <= date_now.hour < 18:
        return "Добрый день"
    elif 18 <= date_now.hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_transactions(file_path: str) -> pd.DataFrame:
    """Загружает данные транзакций из Excel файла."""
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        logger.error(f"Ошибка загрузки транзакций: {e}")
        return pd.DataFrame()

def get_operations_with_range(operations_df: pd.DataFrame, date_end: str) -> pd.DataFrame:
    """Возвращает операции в заданном диапазоне дат."""
    operations_df['Дата операции'] = pd.to_datetime(operations_df['Дата операции'], dayfirst=True)
    first_date = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-01 09:00:00")
    df_filter = operations_df[
        (operations_df["Дата операции"] >= pd.to_datetime(first_date)) &
        (operations_df["Дата операции"] <= pd.to_datetime(date_end))
        ]
    return df_filter

def calculate_cards_summary(df):
    """Рассчитывает и возвращает статистику по картам: последние 4 цифры, общая сумма расходов, кешбэк."""
    filtered_cards = []
    # Отфильтровать по статусу OK и отрицательной сумме (расходы)
    df_filtered = df[(df['Статус'] == 'OK') & (df['Сумма операции'] < 0)]
    # Группируем по последним 4 цифрам карты
    for card_num, group in df_filtered.groupby(df_filtered['Номер карты'].str[-4:]):
        total_spent = float(-group['Сумма операции'].sum())  # суммы отрицательные, берем модуль
        cashback = total_spent / 100  # 1 рубль кешбэк на 100 рублей
        filtered_cards.append({
            "last_digits": card_num,
            "total_spent": round(total_spent, 2),
            "cashback": round(cashback, 2)
        })
    return filtered_cards


def get_top_transactions(df, top_n=5):
    """Возвращает топ-5 транзакций по сумме платежа."""
    # Сортируем по сумме платежа по модулю (абсолютное значение) и берем топ N
    df_sorted = df.copy()
    df_sorted['abs_amount'] = df_sorted['Сумма платежа'].abs()
    df_sorted = df_sorted.sort_values('abs_amount', ascending=False).head(top_n)
    transactions = []
    for _, row in df_sorted.iterrows():
        transactions.append({
            "date": row['Дата операции'].strftime('%d.%m.%Y'),
            "amount": round(row['Сумма платежа'], 2),
            "category": row['Категория'],
            "description": row['Описание']
        })
    return transactions


def fetch_currency_rates(currencies):
    """Возвращает курсы валют из настроек пользователя."""
    rates = []
    base_currency = "RUB"  # базовая валюта для курса
    try:
        response = requests.get(f"https://api.exchangerate.host/latest?base={base_currency}")
        data = response.json()
        for cur in currencies:
            rate = data['rates'].get(cur)
            if rate:
                rates.append({"currency": cur, "rate": round(1 / rate, 2)})  # курс к RUB
    except Exception as e:
        logger.error(f"Ошибка при запросе курсов валют: {e}")
    return rates


def fetch_stock_prices(stocks):
    """Возвращает цены акций из настроек пользователя."""
    prices = []
    api_key = "demo"
    url_template = "https://financialmodelingprep.com/api/v3/quote/{}?apikey=" + api_key
    try:
        for stock in stocks:
            response = requests.get(url_template.format(stock))
            data = response.json()
            if data and isinstance(data, list):
                prices.append({
                    "stock": stock,
                    "price": round(data[0].get('price', 0), 2)
                })
    except Exception as e:
        logger.error(f"Ошибка при запросе цен акций: {e}")
    return prices


# Пример вызова
if __name__ == "__main__":
    result = load_transactions(PATH_TO_OPERATIONS)
    operations_range = get_operations_with_range(result, "2020-12-21 10:15:00")
    # print(operations_range)
    # print(result)
    # greeting = get_greeting("2021-12-21 10:15:00")
    # print(greeting)
    cards_summary = calculate_cards_summary(operations_range)
    # print(json.dumps(cards_summary, ensure_ascii=False, indent=2))


    top_transactions = get_top_transactions(operations_range, top_n=5)
    # print(json.dumps(top_transactions, ensure_ascii=False, indent=2))
    #
    # currency_rates = fetch_currency_rates(USER_SETTINGS["user_currencies"])
    # print(json.dumps(currency_rates, ensure_ascii=False, indent=2))
    #
    # stock_prices = fetch_stock_prices(USER_SETTINGS["user_stocks"])
    # print(json.dumps(stock_prices, ensure_ascii=False, indent=2))

    currency_rates = fetch_currency_rates(USER_SETTINGS["user_currencies"])
    print(json.dumps(currency_rates, ensure_ascii=False, indent=2))