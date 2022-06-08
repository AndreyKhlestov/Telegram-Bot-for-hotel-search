from typing import Tuple
from utils.request_to_api import request_to_api
from utils.data import get_data
from config_data import config
import re
import json


def search_hotel(user_id: int, chat_id: int) -> Tuple[str, int]:
    date_check_in = get_data(user_id, chat_id, 'check_In')
    date_check_out = get_data(user_id, chat_id, 'check_Out')
    num_days = date_check_out - date_check_in
    num_days = num_days.days




    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": f"{get_data(user_id, chat_id, 'destination_Id')}",
                   "pageNumber": "1",
                   "pageSize": f"{get_data(user_id, chat_id, 'num_hotels')}",
                   "checkIn": f"{date_check_in}",
                   "checkOut": f"{date_check_out}",
                   "adults1": "1",

                   "sortOrder": "PRICE",
                   "locale": config.LOCALE,
                   "currency": config.CURRENCY}

    querystring = {"destinationId": "1506246",
                   "pageNumber": "1",
                   "pageSize": "25",
                   "checkIn": "2020-01-08",
                   "checkOut": "2020-01-15",
                   "adults1": "1",
                   "priceMin": "100",
                   "priceMax": "5000",
                   "sortOrder": "DISTANCE_FROM_LANDMARK",
                   "locale": "en_US",
                   "currency": "USD"}


    response = request_to_api(url, querystring)  # ответ на запрос
    pattern = r'(?<="results":).+?(?=,"pagination")'
    find = re.search(pattern, response.text)

    if find:
        data = json.loads(find[0])  # преобразуем в JSON формат

        if data:  # Если что-то нашел (результат поиска есть)
            for i_data in data:
                price = int(i_data["ratePlan"]["price"]["exactCurrent"])
                text = 'Название отеля: {name_hotel}\n' \
                       'Адрес: {street_Address}\n' \
                       'Расстояние до центра города: {distance}\n' \
                       'Стоимость за ночь: {price} руб\n' \
                       'Общая стоимость: {total_price} руб'\
                    .format(
                        name_hotel=i_data["name"],
                        street_Address=i_data["address"]["streetAddress"],
                        distance=i_data["landmarks"][0]["distance"],
                        price=price,
                        total_price=price * num_days
                        )
                id_hotel = i_data["id"]

                yield text, id_hotel
        else:
            return None
    else:
        raise Exception('В ответе (на запрос "отелей") нет нужного ключа')
