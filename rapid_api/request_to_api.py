import requests
from requests import Response
from config_data import config
from loguru import logger
import time


@logger.catch()
def request_to_api(url: str, querystring: dict) -> Response:
    """Универсальная функция для запросов к rapidapi.com через API"""
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": config.RAPID_API_KEY
    }
    # Парсим (используем таймаут(timeout) у запроса, чтобы не ждать продолжительное время ответа от сервера)
    for _ in range(5):  # Пять попыток запроса
        logger.info('Попытка отправка запроса через API')
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:  # проверка статус кода ответа
            logger.info('Запрос успешно получен')
            return response
        elif response.status_code == 429:
            raise requests.exceptions.ConnectionError('Превышена ежемесячная квота запросов')
        time.sleep(1)
    else:
        raise requests.exceptions.ConnectTimeout('Статус кода запроса не положительный')
