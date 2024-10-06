import csv

import pandas as pd



def read_excel_file(file: str) -> list[dict]:
    """Функция считывает файл excel и возвращает список словарей"""
    df = pd.read_excel(file)
    result = []
    row_count = len(df)
    for n in range(0, row_count):
        row_dict = {
            "id": df.at[n, "id"],
            "state": df.at[n, "state"],
            "date": df.at[n, "date"],
            "operationAmount": {
                "amount": df.at[n, "amount"],
                "currency": {
                    "name": df.at[n, "currency_name"],
                    "code": df.at[n, "currency_code"],
                },
            },
            "description": df.at[n, "description"],
            "from": df.at[n, "from"],
            "to": df.at[n, "to"],
        }
        result.append(row_dict)
    return result


if __name__ == "__main__":
    result = read_excel_file("../data/operations.xlsx")
    print(result)