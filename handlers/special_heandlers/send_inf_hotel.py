from loader import bot
from utils.data import get_data
from utils.search_hotel import search_hotel
from utils.get_photo import get_photos
from loguru import logger
from telebot.apihelper import ApiTelegramException
from handlers.special_heandlers.finish_work import finish_work
import requests
import time
import re
from database.models import HotelRequest, Hotel
import datetime


@logger.catch()
def start_send_hotel_inf(user_id: int, chat_id: int) -> None:
    """Начало процедуры отправки информации об найденных отелях"""
    logger.info('Начало процедуры отправки информации об найденных отелях')

    # Сохраняем в базу о запросах и одновременно получаем id запроса
    request_id = HotelRequest.create(user_id=user_id,
                                     command=get_data(user_id, chat_id, 'commands'),
                                     location=get_data(user_id, chat_id, 'location'),
                                     main_info=get_data(user_id, chat_id, 'main_info'),
                                     date=datetime.datetime.now().strftime('%Y.%m.%d  %H:%M:%S')
                                     ).id

    count_hotel = 0
    page_number = 0
    num_hotels = int(get_data(user_id, chat_id, 'num_hotels'))
    my_command = get_data(user_id, chat_id, 'commands')

    if my_command == "bestdeal":
        pattern = r'(?<=Расстояние до центра города: ).+?(?= км)'
        dis_min = int(get_data(user_id, chat_id, 'distance_min'))
        dis_max = int(get_data(user_id, chat_id, 'distance_max'))

    # Т.к. при выполнении команды bestdeal, не все отели могут попасть в веденный пользователем промежуток расстояния
    # до центра города, то считаем сколько отелей попало в промежуток, а если одного запроса не хватило,
    # то запрашиваем следующую страницу отелей
    while count_hotel < num_hotels:
        page_number += 1
        #Отправка текста и стикера поиска
        message_with_stic = bot.send_message(user_id, 'Веду поиск отелей')
        sticker = bot.send_sticker(chat_id,
                                   'CAACAgIAAxkBAAEFJudiu0z--ent9HLJbsxM7S9nAQjK1QACIwADKA9qFCdRJeeMIKQGKQQ')

        inf_hotels = search_hotel(user_id, chat_id, page_number)

        # Удаление текста и стикера поиска
        bot.delete_message(message_with_stic.chat.id, message_with_stic.id)
        bot.delete_message(sticker.chat.id, sticker.id)

        if inf_hotels:
            for text, id_hotel in inf_hotels:

                if my_command == "bestdeal":
                    dis = float(re.search(pattern, text)[0].replace(',', '.'))  # получаем расстояние до центра города
                    if not dis_min <= dis <= dis_max:  # Если расстояние не входит в промежуток введенный пользователем
                        if dis > dis_max:  # Если расстояние больше максимального
                            num_hotels = count_hotel
                            break
                        else:
                            continue

                send_hotel_inf(user_id, chat_id, text, id_hotel)

                # Сохраняем в базу о найденных отелях
                Hotel.create(request_id=request_id,
                             num_queue=count_hotel,
                             hotel_info=text
                             )
                count_hotel += 1

                if count_hotel >= num_hotels:
                    break
        else:
            break

    if 0 < count_hotel < int(get_data(user_id, chat_id, 'num_hotels')):
        bot.send_message(user_id, '⚠ К сожалению, больше нет отелей подходящих по заданным критериям')
    elif count_hotel == 0:
        #  удаляем запрос из базы (запросов отелей) как ненужный
        HotelRequest.delete().where(HotelRequest.id == request_id).execute()
        bot.send_message(user_id, '⚠ К сожалению, нет отелей подходящих по заданным критериям')

    finish_work(user_id, chat_id)


@logger.catch()
def send_hotel_inf(user_id: int, chat_id: int, text: str, id_hotel: str):
    """Функция для отправки информации об найденных отелях"""
    logger.info('Отправка информации об найденных отелях')
    quantity_photo = get_data(user_id, chat_id, 'num_photo')  # Количество фото для вывода (str или None)

    try:
        if quantity_photo:
            list_url_photo = get_photos(id_hotel, quantity_photo)
            if list_url_photo == None:
                bot.send_message(user_id, "⚠ К сожалению, у отеля нет фото")
            elif int(quantity_photo) == 1:
                bot.send_photo(chat_id, list_url_photo[0].media)
            else:
                bot.send_media_group(chat_id, list_url_photo[:int(quantity_photo)])
    except (KeyError, requests.exceptions.ConnectTimeout, ApiTelegramException):
        bot.send_message(user_id, "⚠ К сожалению, не удалось загрузить фото. Но их можно посмотреть на сайте перейдя по"
                                  " ссылке")

    finally:

        time.sleep(1.1)
        bot.send_message(user_id, text)

