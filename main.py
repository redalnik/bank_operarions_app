import json

import pandas as pd

from src.reports import convert_log_to_excel, spending_by_category
from src.services import categories_cashback
from src.views import get_views

df = pd.read_excel("data/operations.xlsx")
with open("data/user_settings.json", "r", encoding="utf-8") as f:
    user_setting = json.load(f)

if __name__ == "__main__":
    user_input = input("Введите дату в формате: YYYY-MM-DD HH:MM:SS - ")
    # вывод результата: Страница «Главная»
    print(get_views(df, user_setting, user_input))
    user_input = input("Проверить выгодные категории повышенного кешбэка? Да/Нет - ").strip().lower()

    if user_input == "да":
        input_year = input("Введите год в формате: YYYY - ")
        input_month = input("Введите месяц в формате: MM - ")
        # вывод результата: Выгодные категории повышенного кешбэк
        print(categories_cashback(df, input_year, input_month))
    else:
        print("Вы пропустили данный пункт")
    user_input = input("Проверить траты по заданной категории за 3 месяца? Да/Нет - ").strip().lower()

    if user_input == "да":
        user_date = input("Введите дату конца периода в формате: YYYY-MM-DD - ")
        user_category = input("Введите категорию - ")
        # вывод результата траты по заданной категории
        print(spending_by_category(df, user_category, user_date, save_to_file=True))
    else:
        print("Вы пропустили данный пункт")

    convert_log_to_excel()
