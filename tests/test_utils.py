# import pandas as pd
#
# from src.utils import get_cards_summary, get_top_transactions
# from src.utils import greeting
#
#
# def test_greeting():
#     assert greeting("2023-09-20 06:00:00") == "Доброе утро"
#     assert greeting("2023-09-20 12:00:00") == "Добрый день"
#     assert greeting("2023-09-20 18:00:00") == "Добрый вечер"
#     assert greeting("2023-09-20 00:00:00") == "Доброй ночи"
#
#
# def test_get_cards_summary():
#     test_data = pd.DataFrame({
#         'Номер карты': ['*7197', '*7197', '*5091', ''],
#         'Сумма платежа': [-100.0, -200.0, -50.0, -30.0],
#         'Категория': ['Супермаркеты', 'Супермаркеты', 'Топливо', 'Переводы']
#     })
#     result = get_cards_summary(test_data)
#     assert len(result) == 3
#     for card in result:
#         assert 'last_digits' in card
#         assert 'total_spent' in card
#         assert 'cashback' in card
#         assert card['cashback'] == card['total_spent'] / 100
#
#
# def test_get_top_transactions():
#     test_data = pd.DataFrame({
#         'Дата операции': [
#             '31.12.2021 16:44:00',
#             '31.12.2021 16:42:04',
#             '30.12.2021 22:22:03',
#             '29.12.2021 10:00:00'
#         ],
#         'Сумма платежа': [-160.89, -20000.00, 15000.00, -500.00],
#         'Категория': ['Супермаркеты', 'Переводы', 'Пополнения', 'Топливо'],
#         'Описание': ['Колхоз', 'Константин Л.', 'Пополнение счета', 'Заправка']
#     })
#
#     result = get_top_transactions(test_data, top_n=2)
#     assert len(result) == 2
#     for transaction in result:
#         assert transaction['amount'] < 0, f"Транзакция должна быть отрицательной: {transaction}"
#
#     assert abs(result[0]['amount']) >= abs(result[1]['amount'])
#
#     assert result[0]['amount'] == -20000.00
#     assert result[1]['amount'] == -500.00
#
#     positive_amounts = [t['amount'] for t in result if t['amount'] > 0]
#     assert len(positive_amounts) == 0
#     positive_amounts = [t['amount'] for t in result if t['amount'] > 0]
#     assert len(positive_amounts) == 0, "Не должно быть положительных сумм"
#
#
