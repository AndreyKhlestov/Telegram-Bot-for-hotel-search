from rapid_api.request_to_api import request_to_api
from utils.data import get_data
from config_data import config
from loguru import logger
import requests
import re
import json
import locale


@logger.catch(reraise=True)
def search_hotel(user_id: int, chat_id: int, page_number: int = 1) -> list or None:
    """Функция для запроса отелей и вывода найденной информации в списке про каждый отель отдельно (отредактированный
    текст для отправки пользователю и id отеля (для дальнейшего поиска фото))"""
    logger.info('Запрос отелей')
    locale.setlocale(locale.LC_ALL, f"{config.LOCALE}.UTF-8")  # для наглядного отображения цены (по три символа)

    date_check_in = get_data(user_id, chat_id, 'check_In')
    date_check_out = get_data(user_id, chat_id, 'check_Out')
    num_days = date_check_out - date_check_in
    num_days = num_days.days

    my_command = get_data(user_id, chat_id, 'commands')

    querystring = {"destinationId": f"{get_data(user_id, chat_id, 'destination_Id')}",
                   "pageNumber": str(page_number),
                   "pageSize": "25",
                   "checkIn": f"{date_check_in}",
                   "checkOut": f"{date_check_out}",
                   "adults1": "1",
                   "locale": config.LOCALE,
                   "currency": config.CURRENCY}

    if my_command == "bestdeal":
        sort_order = "DISTANCE_FROM_LANDMARK"
        querystring["priceMin"] = get_data(user_id, chat_id, 'price_min')
        querystring["priceMax"] = get_data(user_id, chat_id, 'price_max')

    elif my_command == "lowprice":
        sort_order = "PRICE"

    else:
        sort_order = "PRICE_HIGHEST_FIRST"
    querystring["sortOrder"] = sort_order

    url = "https://hotels4.p.rapidapi.com/properties/list"

    response = request_to_api(url, querystring)  # ответ на запрос

    if not response:
        raise requests.ConnectionError('Сбой при получении запроса')

    pattern = r'(?<="results":).+?(?=,"pagination")'

    find = re.search(pattern, response.text)

    if find:
        data = json.loads(find[0])  # преобразуем в JSON формат
        if data:  # Если что-то нашел (результат поиска есть)
            inf_hotel = list()
            for i_data in data:
                id_hotel = i_data["id"]

                price = int(i_data["ratePlan"]["price"]["exactCurrent"]) if "ratePlan" in i_data.keys() else 0
                text = '🏨 Название отеля: {name_hotel}\n\n' \
                       '⭐ Рейтинг: {rating}\n\n' \
                       '🗺 Адрес: {street_Address}\n\n' \
                       '🚗 Расстояние до центра города: {distance}\n\n' \
                       '💵 Стоимость за ночь: {price}\n\n' \
                       '💰 Общая стоимость за {num_days} дн: {total_price}\n\n' \
                       '🌐 Ссылка: {url}'\
                    .format(
                        name_hotel=i_data["name"],
                        rating=i_data["guestReviews"]["rating"] if "guestReviews" in i_data.keys() else '-',
                        street_Address=i_data["address"]["streetAddress"] if "streetAddress" in i_data["address"].keys() else '-',
                        distance=i_data["landmarks"][0]["distance"] if "landmarks" in i_data.keys() else '-',
                        price=f'{price:n} руб' if price != 0 else 'не указана',
                        num_days=num_days,
                        total_price=f'{(price * num_days):n} руб' if price != 0 else '-',
                        url="https://www.hotels.com/ho" + str(id_hotel)
                        )

                inf_hotel.append((text, id_hotel))
            return inf_hotel
        else:
            return None
    else:
        return None
