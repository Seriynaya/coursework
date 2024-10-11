import json

from config import PATH_TO_FILE
from src.utils import read_excel_file
from src.services import search_str
operations_list = read_excel_file(PATH_TO_FILE)
empty_list = []


def test_search_str():
    """Тест функции простой поиск"""
    try:
        assert search_str(operations_list, "Ozon.ru") == json.dumps([
            {
                "Payment data": "31.12.2021",
                "Status": "OK",
                "Payment amount": -564.0,
                "Payment currency": "RUB",
                "Category": "Различные товары",
                "Description": "Ozon.ru",
                "Card number": "*5091"
            },
            {
                "Payment data": "20.12.2021",
                "Status": "OK",
                "Payment amount": 421.0,
                "Payment currency": "RUB",
                "Category": "Различные товары",
                "Description": "Ozon.ru",
                "Card number": "*7197"
            },
            {
                "Payment data": "14.12.2021",
                "Status": "OK",
                "Payment amount": -421.0,
                "Payment currency": "RUB",
                "Category": "Различные товары",
                "Description": "Ozon.ru",
                "Card number": "*7197"
            },
            {
                "Payment data": "21.10.2021",
                "Status": "OK",
                "Payment amount": -119.0,
                "Payment currency": "RUB",
                "Category": "Различные товары",
                "Description": "Ozon.ru",
                "Card number": "*7197"
            },
            {
                "Payment data": "04.10.2020",
                "Status": "OK",
                "Payment amount": -750.0,
                "Payment currency": "RUB",
                "Category": "Различные товары",
                "Description": "Ozon.ru",
                "Card number": "*7197"
            }
        ], indent=4,
            ensure_ascii=False, )
    except Exception as e:
        print("Ошибка")


def test_search_str_empty_attribute():
    """Тест функции простой поиск с пустыми атрибутами """
    assert search_str(empty_list, "Ozon.ru") == json.dumps([], indent=4,
                                                              ensure_ascii=False, )
    assert search_str(operations_list, "") == []