import requests
from rapid_api.request_to_api import request_to_api
from config_data import config
import re
import json
from loguru import logger


@logger.catch()
def edit_text(text: str) -> str:
    """Функция для редактирования данных (из 'caption') в читаемы вид"""
    text = re.sub("<span class='highlighted'>", '', text)
    text = re.sub("</span>", '', text)
    # костыль для случаев, когда город указан несколько раз
    # (например: "Manhattan, New York, New York, United States of America")
    list_text = text.split(', ')
    for world in list_text:
        if list_text.count(world) > 1:
            list_text.remove(world)
    text = ', '.join(list_text)

    return text


@logger.catch(reraise=True)
def search_city(city: str) -> tuple or None:
    """Функция для поиска города.
    Все найденные данные сохраняет в словарь (где ключ - 'destinationId', значение - расположение (данные из "caption"))
    и возвращает его"""
    logger.info('Запрос города')
    name_city = city
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": name_city, "locale": config.LOCALE, "currency": config.CURRENCY}

    response = request_to_api(url, querystring)  # ответ на запрос

    if not response:
        raise requests.ConnectionError('Сбой при получении запроса')

    # проверка в тексте ответа регулярным выражением (на случай, если не будет ключа)
    pattern = r'(?<="CITY_GROUP","entities":).+?[\]]'
    find = re.search(pattern, response.text)
    if find:
        data = json.loads(find[0])  # преобразуем в JSON формат
        if data:  # Если что-то нашел (результат поиска есть)
            # словарь для городов, ключ - 'destinationId', значение - расположение (данные из "caption")
            found_cities_dict = dict()
            for elem in data:  # Проходим по всем вариантам ответа и собираем информацию
                found_cities_dict[elem['destinationId']] = edit_text(elem["caption"])
            return found_cities_dict
        else:
            return None
    else:
        raise KeyError('В ответе (на запрос "города") нет нужного ключа')
