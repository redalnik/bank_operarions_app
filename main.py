import json

import pandas as pd

from src.reports import convert_log_to_excel, spending_by_category
from src.services import categories_cashback
from src.views import get_views

df = pd.read_excel("data/operations.xlsx")
with open("data/user_settings.json", "r", encoding="utf-8") as f:
    user_setting = json.load(f)

if __name__ == "__main__":
    user_input = input("Введите дату в формате: гггг-мм-дд чч:мм:сс - ")
    # вывод результата: Страница «Главная»
    print(get_views(df, user_setting, user_input))
    user_input = input("желаете проверить Выгодные категории повышенного кешбэка? да/нет - ").strip().lower()

    if user_input == "да":
        input_year = input("введите год в формате: гггг - ")
        input_month = input("введите месяц в формате: мм - ")
        # вывод результата: Выгодные категории повышенного кешбэк
        print(categories_cashback(df, input_year, input_month))
    else:
        print("вы пропустили данный пункт")
    user_input = input("желаете проверить траты по заданной категории за 3 месяца? да/нет - ").strip().lower()

    if user_input == "да":
        user_date = input("Введите дату конца периода в формате: гггг-мм-дд - ")
        user_category = input("введите категорию - ")
        # вывод результата траты по заданной категории
        print(spending_by_category(df, user_category, user_date, save_to_file=True))
    else:
        print("вы пропустили данный пункт")

    convert_log_to_excel()
