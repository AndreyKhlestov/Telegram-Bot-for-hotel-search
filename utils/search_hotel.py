from rapid_api.request_to_api import request_to_api
from utils.data import get_data
from config_data import config
from loguru import logger
from loader import bot
from handlers.special_heandlers.finish_work import finish_work
import requests
import re
import json


@logger.catch()
def search_hotel(user_id: int, chat_id: int, page_number: int = 1) -> list or None:
    """Функция для запроса отелей и вывода найденной информации в списке про каждый отель отдельно (отредактированный
    текст для отправки пользователю и id отеля (для дальнейшего поиска фото))"""
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
    try:
        response = request_to_api(url, querystring)  # ответ на запрос

    except requests.exceptions.ConnectTimeout:
        bot.send_message(user_id, 'К сожалению, сервер не отвечает. Попробуйте позже.')
        finish_work(user_id, chat_id)

    else:
        pattern = r'(?<="results":).+?(?=,"pagination")'
        find = re.search(pattern, response.text)

        if find:
            data = json.loads(find[0])  # преобразуем в JSON формат
            if data:  # Если что-то нашел (результат поиска есть)
                inf_hotel = list()
                for i_data in data:
                    id_hotel = i_data["id"]

                    price = int(i_data["ratePlan"]["price"]["exactCurrent"])
                    text = '🏨 Название отеля: {name_hotel}\n\n' \
                           '⭐ Рейтинг: {rating}\n\n' \
                           '🗺 Адрес: {street_Address}\n\n' \
                           '🚗 Расстояние до центра города: {distance}\n\n' \
                           '💵 Стоимость за ночь: {price} руб\n\n' \
                           '💰 Общая стоимость: {total_price} руб\n\n' \
                           '🌐 Ссылка: {url}'\
                        .format(
                            name_hotel=i_data["name"],
                            rating=i_data["guestReviews"]["rating"] if "guestReviews" in i_data.keys() else '-',
                            street_Address=i_data["address"]["streetAddress"] if "streetAddress" in i_data["address"].keys() else '-',
                            distance=i_data["landmarks"][0]["distance"],
                            price=price,
                            total_price=price * num_days,
                            url="https://www.hotels.com/ho" + str(id_hotel)
                            )

                    inf_hotel.append((text, id_hotel))
                return inf_hotel
            else:
                return None
        else:  # В ответе (на запрос "отелей") нет нужного ключа (т.к. ничего не нашел)
            return None
