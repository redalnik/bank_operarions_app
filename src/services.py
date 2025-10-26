import calendar
import logging
import re
from datetime import datetime

import pandas as pd


def categories_cashback(transactions: pd.DataFrame, year: str, month: str) -> dict:
    """
    Рассчитывает потенциальный кэшбэк по категориям за выбранный месяц.
    """
    df = transactions.copy()
    logging.info(f"Рассчитан кэшбэк по категориям за {year}-{month}")
    end_day = calendar.monthrange(int(year), int(month))[1]
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    start = f"{year}-{month}-01"
    end = f"{year}-{month}-{end_day}"
    filtered_df_date = df[df["Дата платежа"].between(start, end)]
    filtered_df_negative = filtered_df_date[filtered_df_date["Сумма платежа"] < 0]
    result_df = (
        filtered_df_negative.groupby("Категория")["Сумма платежа"].sum().abs()
    )
    totals_by_category = result_df.to_dict()
    result: dict = {}
    for category, amount in totals_by_category.items():
        result[category] = int(amount / 100)
    return result


def find_p2p_transfers(transactions: pd.DataFrame) -> list[dict]:
    """
    Возвращает транзакции переводов физическим лицам.

    Условие: категория "Переводы" и в описании имя и первая буква фамилии с точкой (например: "Иван П.").
    """
    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True, errors="coerce")
    pattern = re.compile(r"^[А-ЯA-ZЁ][а-яa-zё]+\s[А-ЯA-ZЁ]\.")
    filtered = df[(df["Категория"].astype(str) == "Переводы") & (df["Описание"].astype(str).str.match(pattern))]
    result = [
        {
            "date": (
                row["Дата операции"].strftime("%Y-%m-%d")
                if isinstance(row["Дата операции"], datetime)
                else str(row["Дата операции"])
            ),
            "amount": row.get("Сумма платежа"),
            "description": row.get("Описание", ""),
        }
        for _, row in filtered.iterrows()
    ]
    logging.info(f"Найдено переводов физлицам: {len(result)}")
    return result
