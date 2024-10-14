import json

import pandas as pd
import pytest

from src.reports import transactions_amount_3_months

from tests.confitest import test_df
def test_transactions_amount_3_months(test_df):
    """Тест вывода трат по категории"""
    new_df = transactions_amount_3_months(test_df, "Супермаркеты", "2021-12-31 14:46:24")
    sorted_list_category = new_df.to_dict(orient="records")
    assert sorted_list_category == [
        {"Transaction date": "31.12.2021", "Transaction amount": -160.89, "Category": "Супермаркеты"},
        {"Transaction date": "31.12.2021", "Transaction amount": -64.0, "Category": "Супермаркеты"},
        {"Transaction date": "31.12.2021", "Transaction amount": -118.12, "Category": "Супермаркеты"},
        {"Transaction date": "19.11.2021", "Transaction amount": -339.9, "Category": "Супермаркеты"},
    ]


def test_transactions_amount_3_months_with_incorrect_date(capsys, test_df):
    """Тест вывода сообщения при ошибке формата даты"""
    assert (transactions_amount_3_months(test_df, "Супермаркеты", "31-12-2021")).to_dict(orient="records") == []
    result = capsys.readouterr()
    assert result.out == "Некорректный формат даты\nФормирование отчёта завершено\n"


def test_transactions_amount_3_months_with_incorrect_category(capsys, test_df):
    """Тест вывода сообщения при ошибке ввода категории"""
    assert (transactions_amount_3_months(test_df, "Супермаркет", "2021-12-31 14:46:24")).to_dict(orient="records") == []
    result = capsys.readouterr()
    assert result.out == "Неверно введена категория\nФормирование отчёта завершено\n"