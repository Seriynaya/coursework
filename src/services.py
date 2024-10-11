import datetime
import json
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(BASE_DIR, "logs", "services.log")

logger = logging.getLogger("services")
file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def search_str(operations_list: list, str_search: str):
    """Функция поиска по переданной строке"""
    result = []
    logger.info("Начало работы")
    for info in operations_list:
        if str_search == "":
            return result
        elif str_search in info["Description"] or str_search in info["Category"]:
            result.append(info)
        else:
            return result
    logger.info("Данные по переданной строке сформированны")
    json_report_format = json.dumps(
        result,
        indent=4,
        ensure_ascii=False,
    )

    return json_report_format
