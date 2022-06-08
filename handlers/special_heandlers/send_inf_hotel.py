from loader import bot
from states.user_states import UserState
from utils.data import get_data
from utils.search_hotel import search_hotel
from utils.get_photo import get_photos
from loguru import logger
import re


@logger.catch()
def send_hotel_inf(user_id: int, chat_id: int) -> None:
    """Функция для отправки информации об найденных отелях"""
    bot.send_message(user_id, 'Вот, что я нашел:')

    if get_data(user_id, chat_id, 'commands') == "bestdeal":
        page_number = 0
        count_hotel = 0
        num_hotels = int(get_data(user_id, chat_id, 'num_hotels'))
        pattern = r'(?<=Расстояние до центра города: ).+?(?= км)'
        dis_min = int(get_data(user_id, chat_id, 'distance_min'))
        dis_max = int(get_data(user_id, chat_id, 'distance_max'))

        while count_hotel < num_hotels:
            page_number += 1
            for text, id_hotel in search_hotel(user_id, chat_id, page_number):

                dis = float(re.search(pattern, text)[0].replace(',', '.'))

                if dis_min <= dis <= dis_max:
                    send(user_id, chat_id, text, id_hotel)
                    count_hotel += 1
                    if count_hotel >= num_hotels:
                        break
    else:
        for text, id_hotel in search_hotel(user_id, chat_id):
            # if quantity_photo:
            #     list_url_photo = get_photos(id_hotel, quantity_photo)
            #     if int(quantity_photo) == 1:
            #         bot.send_photo(chat_id, list_url_photo[0].media)
            #     else:
            #         bot.send_media_group(chat_id, list_url_photo)
            # bot.send_message(user_id, text)
            send(user_id, chat_id, text, id_hotel)
    bot.set_state(user_id, UserState.finish, chat_id)


def send(user_id: int, chat_id: int, text: str, id_hotel: str):
    quantity_photo = get_data(user_id, chat_id, 'num_photo')  # Количество фото для вывода (str или None)
    if quantity_photo:
        list_url_photo = get_photos(id_hotel, quantity_photo)
        if int(quantity_photo) == 1:
            bot.send_photo(chat_id, list_url_photo[0].media)
        else:
            bot.send_media_group(chat_id, list_url_photo)
    bot.send_message(user_id, text)