import json
from datetime import datetime
import utils  # импорт вспомогательных функций из модуля utils1.py

def main_view(input_datetime: str) -> str:
    """
    Функция для страницы "Главная".
    Принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS,
    возвращает JSON-строку с приветствием, суммами по картам, топ-5 транзакций,
    курсами валют и ценами акций.
    """
    #
    # try:
    #     # Парсим входящую дату
    #     date_now = datetime.strptime(input_datetime, '%Y-%m-%d %H:%M:%S')
    # except ValueError:
    #     return json.dumps({"error": "Неверный формат даты, ожидается YYYY-MM-DD HH:MM:SS"}, ensure_ascii=False)

    # Загрузка всех транзакций (например, из Excel)
    df = utils.load_transactions()
    if df.empty:
        return json.dumps({"error": "Данные транзакций не загружены"}, ensure_ascii=False)

    # Получаем приветствие по времени
    greeting = utils.get_greeting(input_datetime)

    # Рассчитываем сумму расходов и кешбэк по каждой карте
    cards_summary = utils.calculate_cards_summary(df)

    # Получаем топ-5 транзакций по сумме платежа
    top_transactions = utils.get_top_transactions(df, top_n=5)

    # Получаем курсы валют из настроек пользователя
    currency_rates = utils.fetch_currency_rates()

    # Получаем цены акций из настроек пользователя
    stock_prices = utils.fetch_stock_prices()

    # Формируем итоговый ответ
    response = {
        "greeting": greeting,
        "cards": cards_summary,
        "top_transactions": top_transactions,
        # "currency_rates": currency_rates,
        # "stock_prices": stock_prices
    }

    return json.dumps(response, ensure_ascii=False, indent=2)




# def main_view(input_datetime_str):
#     try:
#         input_datetime = datetime.strptime(input_datetime_str, '%Y-%m-%d %H:%M:%S')
#     except ValueError as e:
#         logger.error(f"Неверный формат даты: {input_datetime_str}")
#         return json.dumps({"error": "Неверный формат даты, ожидается YYYY-MM-DD HH:MM:SS"}, ensure_ascii=False)
#
#     df = load_transactions()
#     if df.empty:
#         return json.dumps({"error": "Данные транзакций не загружены"}, ensure_ascii=False)
#
#     greeting = get_greeting(input_datetime)
#     cards_summary = calculate_cards_summary(df)
#     top_transactions = get_top_transactions(df)
#     currency_rates = fetch_currency_rates(USER_SETTINGS["user_currencies"])
#     stock_prices = fetch_stock_prices(USER_SETTINGS["user_stocks"])
#
#     response = {
#         "greeting": greeting,
#         "cards": cards_summary,
#         "top_transactions": top_transactions,
#         "currency_rates": currency_rates,
#         "stock_prices": stock_prices
#     }
#
#     return json.dumps(response, ensure_ascii=False, indent=2)
