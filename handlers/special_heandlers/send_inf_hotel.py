from loader import bot
from states.user_states import UserState
from utils.data import get_data
from utils.search_hotel import search_hotel
from utils.get_photo import get_photos
from loguru import logger
from telebot.apihelper import ApiTelegramException
import requests
import time
import re


@logger.catch()
def start_send_hotel_inf(user_id: int, chat_id: int) -> None:
    """Начало процедуры отправки информации об найденных отелях"""
    bot.send_message(user_id, 'Вот, что я нашел:')
    if get_data(user_id, chat_id, 'commands') == "bestdeal":
        page_number = 0
        count_hotel = 0
        num_hotels = int(get_data(user_id, chat_id, 'num_hotels'))
        pattern = r'(?<=Расстояние до центра города: ).+?(?= км)'
        dis_min = int(get_data(user_id, chat_id, 'distance_min'))
        dis_max = int(get_data(user_id, chat_id, 'distance_max'))

        # Т.к. не все отели могут попасть в веденный пользователем промежуток расстояния до центра города, то считаем
        # сколько отелей попало в промежуток, а если одного запроса не хватило, то запрашиваем следующую страницу отелей
        while count_hotel < num_hotels:
            page_number += 1
            for text, id_hotel in search_hotel(user_id, chat_id, page_number):
                dis = float(re.search(pattern, text)[0].replace(',', '.'))  # получаем расстояние до центра города
                if dis_min <= dis <= dis_max:  # Если расстояние входит в промежуток введенный пользователем
                    send_hotel_inf(user_id, chat_id, text, id_hotel)
                    count_hotel += 1
                    if count_hotel >= num_hotels:
                        break
                if dis > dis_max:
                    count_hotel = num_hotels
                    break

    else:
        for text, id_hotel in search_hotel(user_id, chat_id):
            send_hotel_inf(user_id, chat_id, text, id_hotel)
    bot.set_state(user_id, UserState.finish, chat_id)


@logger.catch()
def send_hotel_inf(user_id: int, chat_id: int, text: str, id_hotel: str):
    """Функция для отправки информации об найденных отелях"""
    quantity_photo = get_data(user_id, chat_id, 'num_photo')  # Количество фото для вывода (str или None)

    try:
        if quantity_photo:
            list_url_photo = get_photos(id_hotel, quantity_photo)
            if list_url_photo == None:
                bot.send_message(user_id, "К сожалению, у отеля нет фото")
            elif int(quantity_photo) == 1:
                bot.send_photo(chat_id, list_url_photo[0].media)
            else:
                bot.send_media_group(chat_id, list_url_photo[:int(quantity_photo)])
    except (KeyError, requests.exceptions.ConnectTimeout, ApiTelegramException):
        bot.send_message(user_id, "К сожалению, не удалось загрузить фото. Но их можно посмотреть на сайте перейдя по "
                                  "ссылке")
    except:
        bot.send_message(user_id, "Что-то пошло не так в модуле 'send_hotel_inf'")
    finally:
        time.sleep(1.5)
        bot.send_message(user_id, text)
