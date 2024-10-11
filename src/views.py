import json

import pandas as pd
from src.utils import (card_info, currency, greetings, prices,
                       top_5_transactions)


def json_report(df: pd.DataFrame, date: str, user_settings):
    """Функция выводящая результат запроса по дате в JSON-формате"""
    transactions = {
        "greeting": greetings(),
        "cards": card_info(date, df),
        "top 5 transactions": top_5_transactions(date, df),
        "currency": currency(user_settings["user_currencies"]),
        "prices": prices(user_settings["user_stocks"]),
    }
    json_report_format = json.dumps(transactions, indent=4, ensure_ascii=False)
    return json_report_format
