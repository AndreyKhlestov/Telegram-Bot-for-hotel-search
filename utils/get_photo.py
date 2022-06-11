from utils.request_to_api import request_to_api
import re
import json
from telebot.types import InputMediaPhoto
from loguru import logger


@logger.catch()
def get_photos(id_hotel: str, quantity_photo: str):

    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": id_hotel}

    response = request_to_api(url, querystring)  # ответ на запрос
    # pattern = r'(?<="roomImages":).+?(?=,"featuredImageTrackingDetails")'
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
            # for i_room in data:
            #     for i_data_room in i_room["images"]:
            #         # url = re.sub("{size}", 'z', i_data_room["baseUrl"])
            #         url = re.sub("{size}", 'd', i_data_room["baseUrl"])
            #         list_of_urls.append(InputMediaPhoto(url))
            #         if len(list_of_urls) == int(quantity_photo):
            #             return list_of_urls
            # return list_of_urls
        else:
            return None
    else:
        return None
        # raise KeyError('В ответе (на запрос "фото отелей") нет нужного ключа')

