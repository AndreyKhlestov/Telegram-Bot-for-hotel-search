from typing import Tuple
from utils.request_to_api import request_to_api
from utils.data import get_data
from config_data import config
from loguru import logger
import re
import json


@logger.catch()
def search_hotel(user_id: int, chat_id: int, page_number: int = 1) -> Tuple[str, int]:
    date_check_in = get_data(user_id, chat_id, 'check_In')
    date_check_out = get_data(user_id, chat_id, 'check_Out')
    num_days = date_check_out - date_check_in
    num_days = num_days.days

    querystring = {"destinationId": f"{get_data(user_id, chat_id, 'destination_Id')}",
                   "pageNumber": str(page_number),
                   "pageSize": f"{get_data(user_id, chat_id, 'num_hotels')}",
                   "checkIn": f"{date_check_in}",
                   "checkOut": f"{date_check_out}",
                   "adults1": "1",
                   "locale": config.LOCALE,
                   "currency": config.CURRENCY}

    if get_data(user_id, chat_id, 'commands') == "bestdeal":
        sort_order = "DISTANCE_FROM_LANDMARK"
        querystring["priceMin"] = get_data(user_id, chat_id, 'price_min')
        querystring["priceMax"] = get_data(user_id, chat_id, 'price_max')
    elif get_data(user_id, chat_id, 'commands') == "lowprice":
        sort_order = "PRICE"
    else:
        sort_order = "PRICE_HIGHEST_FIRST"
    querystring["sortOrder"] = sort_order

    url = "https://hotels4.p.rapidapi.com/properties/list"

    response = request_to_api(url, querystring)  # ответ на запрос
    pattern = r'(?<="results":).+?(?=,"pagination")'
    find = re.search(pattern, response.text)

    if find:
        data = json.loads(find[0])  # преобразуем в JSON формат

        if data:  # Если что-то нашел (результат поиска есть)
            for i_data in data:
                id_hotel = i_data["id"]
                price = int(i_data["ratePlan"]["price"]["exactCurrent"])
                text = 'Название отеля: {name_hotel}\n' \
                       'Адрес: {street_Address}\n' \
                       'Расстояние до центра города: {distance}\n' \
                       'Стоимость за ночь: {price} руб\n' \
                       'Общая стоимость: {total_price} руб\n' \
                       'Ссылка: {url}'\
                    .format(
                        name_hotel=i_data["name"],
                        street_Address=i_data["address"]["streetAddress"],
                        distance=i_data["landmarks"][0]["distance"],
                        price=price,
                        total_price=price * num_days,
                        url="https://www.hotels.com/ho" + str(id_hotel)
                        )

                yield text, id_hotel
        else:
            return None
    else:
        raise Exception('В ответе (на запрос "отелей") нет нужного ключа')
