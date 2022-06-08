import requests
from requests import Response
from config_data import config
from loguru import logger


@logger.catch()
def request_to_api(url: str, querystring: dict) -> Response:
    """Универсальная функция для запросов к API"""
    try:
        headers = {
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
            "X-RapidAPI-Key": config.RAPID_API_KEY
        }
        # Парсим (используем таймаут(timeout) у запроса, чтобы не ждать продолжительное время ответа от сервера)
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)

        if response.status_code == requests.codes.ok:  # проверка статус кода ответа
            return response
        else:
            raise Exception('Статус кода запроса не положительный')
    except Exception:
        raise Exception('Статус кода запроса не положительный')
