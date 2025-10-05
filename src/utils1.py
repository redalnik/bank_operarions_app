# import datetime
# import pandas as pd
# import sys
# from pathlib import Path
#
# # Добавляем корневую директорию в путь
# project_root = Path(__file__).parent.parent
# sys.path.insert(0, str(project_root))
#
# from config import PATH_TO_OPERATIONS, PATH
#
#
# def greeting(date_str: str) -> str:
#     """Рассчитывает и выводит приветствие в зависимости от заданного времени."""
#     date_now = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
#     if 6 <= date_now.hour < 12:
#         return "Доброе утро"
#     elif 12 <= date_now.hour < 18:
#         return "Добрый день"
#     elif 18 <= date_now.hour < 24:
#         return "Добрый вечер"
#     else:
#         return "Доброй ночи"
#
#
# def read_excell_file(file_path: str) -> pd.DataFrame:
#     """Загружает данные из excel файла и возвращает DataFrame."""
#     df = pd.read_excel(file_path)
#     df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
#     return df
#
#
# def get_operations_with_range(operations_df: pd.DataFrame, date_end: str) -> pd.DataFrame:
#     """Возвращает операции в заданном диапазоне дат."""
#     first_date = datetime.datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-01 09:00:00")
#     df_filter = operations_df[
#         (operations_df["Дата операции"] >= pd.to_datetime(first_date)) &
#         (operations_df["Дата операции"] <= pd.to_datetime(date_end))
#         ]
#     return df_filter
#
#
# def get_cards_statistics(operations_df: pd.DataFrame) -> list[dict]:
#     """ Статистика по картам: последние 4 цифры, общая сумма расходов, кешбэк"""
#     operations_df = operations_df[operations_df['Сумма платежа'] < 0]
#     result = []
#     for card_number, group in operations_df.groupby('Номер карты'):
#         last_digits = card_number.replace('*', '')
#         total_spent = float(abs(group['Сумма платежа'].sum()))
#         cashback = total_spent / 100
#         result.append({
#             "last_digits": last_digits,
#             "total_spent": round(total_spent, 2),
#             "cashback": round(cashback, 2)
#         })
#     return result
#
#
# def get_top_transactions(operations_df: pd.DataFrame, top_n: int = 5) -> list[dict]:
#     """Возвращает топ-5 транзакций по сумме платежа."""
#     df = operations_df.copy()
#     df = df[(df['Сумма платежа'].notna()) & (df['Сумма платежа'] < 0)]
#     df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S', dayfirst=True).dt.strftime(
#         "%d.%m.%Y")
#     df['abs_amount'] = df['Сумма платежа'].abs()
#     df = df.sort_values(by='abs_amount', ascending=False)
#     df['Категория'] = df['Категория'].fillna('Без категории')
#     top_df = df.head(top_n)
#     result = []
#     for _, row in top_df.iterrows():
#         result.append({
#             "date": row['Дата операции'],
#             "amount": float(round(row['Сумма платежа'], 2)),
#             "category": row['Категория'],
#             "description": row['Описание']
#         })
#     return result
#
#
# if __name__ == "__main__":
#     data = read_excell_file(PATH_TO_OPERATIONS)
#     # data = read_excell_file(PATH / 'data' / 'operations.xlsx')
#     operations_range = get_operations_with_range(data, "2021-05-20 18:30:00")
#     # print(operations_range)
#     # print(get_cards_statistics(operations_range))
#     print(get_top_transactions(operations_range))
