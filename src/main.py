import pandas as pd
import json

from config import PATH_TO_FILE
from src.reports import transactions_amount_3_months
from src.utils import read_excel_file
from src.views import json_report
from services import search_str

with open("..\\user_settings.json") as file:
    data_file = json.load(file)

def main(date: str, df: pd.DataFrame):
    """Главная функция выводящая результат работы всех функций"""
    print(json_report(df, date, data_file))
    category = input("Введите категорию для фильтрации транзакций: ")
    print(transactions_amount_3_months(df, category, date).to_json(orient="records", indent=4, force_ascii=False))
    str_search = input("Введите строчку для фильтрации транзакций")
    print(search_str(str_search))


if __name__ == "__main__":
    date_str = input("Введите дату в формате: YYYY-MM-DD HH:MM:SS: ")
    print(main(date_str, read_excel_file(PATH_TO_FILE)))