import datetime
import logging
import os
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_RATES_DATA_API = os.getenv("API_KEY_APILAYER")
API = os.getenv("API_KEY_ALPHA_VANTAGE")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(BASE_DIR, "logs", "utils.log")

logger = logging.getLogger("utils")
file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def read_excel_file(path_file: str) -> list[dict]:
    """Функция читает .xlsx файл и возвращает список словарей"""
    df = pd.read_excel(path_file)
    result = df.apply(
        lambda row: {
            "Payment data": row["Дата платежа"],
            "Status": row["Статус"],
            "Payment amount": row["Сумма платежа"],
            "Payment currency": row["Валюта платежа"],
            "Category": row["Категория"],
            "Description": row["Описание"],
            "Card number": row["Номер карты"],
        },
        axis=1,
    ).tolist()
    return result


def greetings():
    """Функция выводит сообщение с приветствием в зависимости от времени суток."""
    greetings_words = {"greeting": ("Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи")}
    current_time = datetime.datetime.now()
    if 4 <= current_time.hour <= 12:
        greet = greetings_words["greeting"][0]
    elif 12 <= current_time.hour <= 16:
        greet = greetings_words["greeting"][1]
    elif 16 <= current_time.hour <= 24:
        greet = greetings_words["greeting"][2]
    else:
        greet = greetings_words["greeting"][3]
    return greet


def card_info(date_str: str, df: pd.DataFrame) -> list[dict[str, Any]]:
    """Функция отображает информацию по карте"""
    try:
        date_str_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
        start_date_for_sorting = date_str_obj.replace(day=1)
        edited_df = df.drop(
            [
                "Payment date",
                "Transaction currency",
                "Payment amount",
                "Payment currency",
                "Cashback",
                "Category",
                "MCC",
                "Description",
                "Bonuses (including cashback)",
                "Rounding to the investment bank",
                "The amount of the operation with rounding",
            ],
            axis=1,
        )
        edited_df["Transaction date"] = edited_df["Transaction date"].apply(
            lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
        )
        filtered_df_by_date = edited_df.loc[
            (edited_df["Transaction date"] <= date_str_obj)
            & (edited_df["Transaction date"] >= start_date_for_sorting)
            & (edited_df["Card number"].notnull())
            & (edited_df["Transaction amount"] <= 0)
            & (edited_df["Status"] != "FAILED")
        ]
        grouped_df = filtered_df_by_date.groupby(["Card number"], as_index=False).agg({"Transaction amount": "sum"})
        grouped_df["Cashback"] = grouped_df["Transaction amount"].apply(lambda x: round(abs(x) / 100, 2))
        grouped_df["Card number"] = grouped_df["Card number"].apply(lambda x: x.replace("*", ""))
        data_list = grouped_df.to_dict("records")
        logger.info("Данные по картам успешно сформированны")
        return data_list

    except ValueError:
        print("Некорректная дата")
        logger.error("Ошибка ввода: некорректная дата")
        return []


def top_5_transactions(date_str: str, df: pd.DataFrame) -> list[dict[str, Any]]:
    """Функция отображения топ 5 транзакций по сумме платежа"""
    try:
        date_str_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
        start_date_month = date_str_obj.replace(day=1)
        edited_df = df.drop(
            [
                "Payment date",
                "Card number",
                "Transaction currency",
                "Payment amount",
                "Payment currency",
                "Cashback",
                "MCC",
                "Bonuses (including cashback)",
                "Rounding to the investment bank",
                "The amount of the operation with rounding",
            ],
            axis=1,
        )
        edited_df["Transaction date"] = edited_df["Transaction date"].apply(
            lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
        )
        filtered_df_by_date = edited_df.loc[
            (edited_df["Transaction date"] <= date_str_obj)
            & (edited_df["Transaction date"] >= start_date_month)
            & (edited_df["Transaction amount"].notnull())
            & (edited_df["Status"] != "FAILED")
        ]
        sorted_df_by_transaction_amount = filtered_df_by_date.sort_values(
            by=["Transaction amount"], ascending=False, key=lambda x: abs(x)
        )
        top_transactions = sorted_df_by_transaction_amount[0:5]
        data_list = []
        for index, row in top_transactions.iterrows():
            data_dict = {
                "date": row["Transaction date"].strftime("%d.%m.%Y"),
                "amount": round(row["Transaction amount"], 2),
                "category": row["Category"],
                "description": row["Description"],
            }
            data_list.append(data_dict)
        logger.info("Данные по топу транзакций успешно сформированны")
    except ValueError:
        logger.error("Ошибка ввода: некорректная дата")
        print("Некорректная дата")
        return []
    else:
        return data_list


def currency(currency_list: list[str]) -> list[dict[str, [str | int]]]:
    """Функция получения курса валют через API"""
    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": f"{EXCHANGE_RATES_DATA_API}"}
    currencies = []
    for currency in currency_list:
        payload = {"symbols": "RUB", "base": f"{currency}"}
        response = requests.get(url, headers=headers, params=payload)
        status_code = response.status_code
        if status_code == 200:
            res = response.json()
            currency_rate_dict = {"currency": f"{res["base"]}", "rate": round(float(res["rates"]["RUB"]), 2)}
            currencies.append(currency_rate_dict)
        else:
            print("Запрос не удался.")
            logger.warning("Запрос не удался")
            return []
    logger.info("Данные по курсу валют сформированны")
    return currencies


def prices(stock_list: list[str]) -> list[dict[str, [str | int]]]:
    """Функция получающая курс акций"""
    stocks_rate = []
    for stock in stock_list:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API}"
        response = requests.get(url)
        status_code = response.status_code
        if status_code == 200:
            res = response.json()
            date = res["Meta Data"]["3. Last Refreshed"]
            new_dict = {"stock": stock, "price": round(float(res["Time Series (Daily)"][f"{date}"]["2. high"]), 2)}
            stocks_rate.append(new_dict)
        else:
            logger.info("Ошибка")
            print("Ошибка")
    logger.info("Данные по курсу акций сформированны")
    return stocks_rate
