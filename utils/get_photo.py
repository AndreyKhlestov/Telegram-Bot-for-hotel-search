from rapid_api.request_to_api import request_to_api
import re
import json
from telebot.types import InputMediaPhoto
from loguru import logger


@logger.catch()
def get_photos(id_hotel: str, quantity_photo: str) -> list or None:
    """Функция для запроса url фото отелей.
    Возвращает список InputMediaPhoto"""
    logger.info('Запрос фото')
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": id_hotel}

    response = request_to_api(url, querystring)  # ответ на запрос
    pattern = r'(?<="hotelImages":).+?(?=,"roomImages")'
    find = re.search(pattern, response.text)
    if find:
        data = json.loads(find[0])  # преобразуем в JSON формат
        if data:  # Если что-то нашел (результат поиска есть)
            list_of_urls = list()

            for i_photo in data[:10]:
                url = re.sub("{size}", i_photo["sizes"][0]["suffix"], i_photo["baseUrl"])
                list_of_urls.append(InputMediaPhoto(url))
            return list_of_urls
        else:
            return None
    else:
        return None
