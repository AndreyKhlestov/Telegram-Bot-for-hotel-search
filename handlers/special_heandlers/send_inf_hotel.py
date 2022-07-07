from loader import bot
from utils.data import get_data, set_data
from keyboards.inline.keyboard_yes_or_no import keyboards_yes_or_no
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
from states.user_states import UserState
from telebot.types import Message, CallbackQuery
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@logger.catch()
def start_send_hotel_inf(user_id: int, chat_id: int) -> None:
    """Начало процедуры отправки информации об найденных отелях"""
    logger.info('Начало процедуры отправки информации об найденных отелях')
    bot.set_state(user_id, UserState.send_inf_hotel, chat_id)
    # Получаем и создаем нужные переменные для работы

    if get_data(user_id, chat_id, 'pageNumber'):  # Если пользователь выбрал вывод доп. отелей по тому же запросу

        request_id = HotelRequest.select().where(HotelRequest.user_id == user_id).order_by(-HotelRequest.date).get().id
        list_id_hotels = [i_hotel.hotel_id for i_hotel in Hotel.select().where(Hotel.request_id == request_id)]
        page_number = int(get_data(user_id, chat_id, 'pageNumber'))  # Номер страницы запроса
        count_hotel = len(Hotel.select().where(Hotel.request_id == request_id))  # Счетчик уже отправленных отелей

    else:  # если новый запрос
        # Сохраняем в базу о запросах и одновременно получаем id запроса
        request_id = HotelRequest.create(user_id=user_id,
                                         command=get_data(user_id, chat_id, 'commands'),
                                         id_location=get_data(user_id, chat_id, 'destination_Id'),
                                         location=get_data(user_id, chat_id, 'location'),
                                         main_info=get_data(user_id, chat_id, 'main_info'),
                                         date=datetime.datetime.now().strftime('%Y.%m.%d  %H:%M:%S')
                                         ).id
        page_number = 1  # Номер страницы запроса
        count_hotel = 0  # Счетчик отправленных отелей
        list_id_hotels = list()  # Список с данными отелей

    num_hotels = int(get_data(user_id, chat_id, 'num_hotels'))  # Нужное количество отелей для вывода
    my_command = get_data(user_id, chat_id, 'commands')  # название команды, который ввел пользователь
    count_repeat_hotels = 0
    status_request = True

    if my_command == "bestdeal":
        pattern = r'(?<=Расстояние до центра города: ).+?(?= км)'  # шаблон для дальнейшего получения расстояния отеля
        dis_min = int(get_data(user_id, chat_id, 'distance_min'))  # минимальное расстояния отеля от центра
        dis_max = int(get_data(user_id, chat_id, 'distance_max'))  # максимальное расстояния отеля от центра

    # Ведем поиск отелей, пока не найдем нужное количество
    while count_hotel < num_hotels:
        # Отправка текста и стикера поиска
        message_with_stic = bot.send_message(user_id, 'Веду поиск отелей')
        sticker = bot.send_sticker(chat_id,
                                   'CAACAgIAAxkBAAEFJudiu0z--ent9HLJbsxM7S9nAQjK1QACIwADKA9qFCdRJeeMIKQGKQQ')
        try:
            inf_hotels = search_hotel(user_id, chat_id, page_number)
        except (KeyError, requests.ConnectionError):
            # Удаление текста и стикера поиска
            bot.delete_message(message_with_stic.chat.id, message_with_stic.id)
            bot.delete_message(sticker.chat.id, sticker.id)

            bot.send_message(user_id, 'К сожалению, сервер не отвечает. Попробуйте позже.')
            status_request = False
            break
        else:
            # Удаление текста и стикера поиска
            bot.delete_message(message_with_stic.chat.id, message_with_stic.id)
            bot.delete_message(sticker.chat.id, sticker.id)

            if inf_hotels:
                if get_data(user_id, chat_id, 'first_index_hotel'):
                    i_start = int(get_data(user_id, chat_id, 'first_index_hotel'))
                    inf_hotels = inf_hotels[i_start:]
                    set_data(user_id, chat_id, 'first_index_hotel', '')

                for index, data in enumerate(inf_hotels):
                    text, id_hotel = data

                    if id_hotel in list_id_hotels:
                        count_repeat_hotels += 1
                        if count_repeat_hotels >= 10:
                            break
                        continue

                    if my_command == "bestdeal":
                        dis = float(re.search(pattern, text)[0].replace(',', '.'))  # расстояние до центра города
                        if not dis_min <= dis <= dis_max:  # расстояние не входит в промежуток введенный пользователем
                            if dis > dis_max:  # Если расстояние больше максимального
                                num_hotels = count_hotel
                                break
                            else:
                                continue
                    quantity_photo = get_data(user_id, chat_id, 'num_photo')  # Кол-во фото для вывода (str или None)
                    try:
                        if quantity_photo:
                            list_url_photo = get_photos(id_hotel, quantity_photo)
                            if list_url_photo is None:
                                bot.send_message(user_id, "⚠ К сожалению, у отеля нет фото")
                            elif int(quantity_photo) == 1:
                                bot.send_photo(chat_id, list_url_photo[0].media)
                            else:
                                bot.send_media_group(chat_id, list_url_photo[:int(quantity_photo)])
                    except (KeyError, requests.exceptions.ConnectTimeout, ApiTelegramException):
                        bot.send_message(user_id,
                                         "⚠ К сожалению, не удалось загрузить фото. Но их можно посмотреть на сайте "
                                         "перейдя по ссылке")

                    time.sleep(1.1)
                    bot.send_message(user_id, text)
                    list_id_hotels.append(id_hotel)  # Добавляем id отеля в список, для будущих проверок отелей

                    # Сохраняем в базу о найденных отелях
                    Hotel.create(request_id=request_id,
                                 hotel_id=id_hotel,
                                 num_queue=count_hotel,
                                 hotel_info=text
                                 )
                    count_hotel += 1

                    if count_hotel == num_hotels:  # Если все нашли
                        if len(inf_hotels) == count_hotel:  # Если использовали весь список отелей
                            set_data(user_id, chat_id, 'first_index_hotel', '')
                            set_data(user_id, chat_id, 'pageNumber', str(page_number + 1))
                        else:
                            set_data(user_id, chat_id, 'first_index_hotel', str(index + 1))
                            set_data(user_id, chat_id, 'pageNumber', str(page_number))
                        break

            else:
                break
            if count_repeat_hotels >= 10:
                break

            page_number += 1

    if status_request:
        if count_hotel == int(get_data(user_id, chat_id, 'num_hotels')):
            bot.send_message(user_id, 'Вывести еще отели?', reply_markup=keyboards_yes_or_no())
        else:
            if 0 < count_hotel < int(get_data(user_id, chat_id, 'num_hotels')):
                bot.send_message(user_id, '⚠ К сожалению, больше нет отелей подходящих по заданным критериям')
            elif count_hotel == 0:
                #  удаляем запрос из базы (запросов отелей) как ненужный
                HotelRequest.delete().where(HotelRequest.id == request_id).execute()
                bot.send_message(user_id, '⚠ К сожалению, нет отелей подходящих по заданным критериям')
            finish_work(user_id, chat_id)
    else:
        finish_work(user_id, chat_id)


@bot.callback_query_handler(func=lambda call: bot.get_state(call.from_user.id, call.message.chat.id) ==
                            'UserState:send_inf_hotel')
@logger.catch()
def callback_send_inf_hotel(call: CallbackQuery) -> None:
    """Функция для обработки ответа пользователя при ответе о выводе доп. отелей"""
    logger.info('Обработка ответа пользователя при ответе о выводе доп. отелей (да/нет)')
    if call.data == 'Да':
        keyboards = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text='3', callback_data='3')
        button_2 = InlineKeyboardButton(text='5', callback_data='5')
        button_3 = InlineKeyboardButton(text='7', callback_data='7')
        button_4 = InlineKeyboardButton(text='10', callback_data='10')
        keyboards.add(button_1, button_2, button_3, button_4)
        bot.edit_message_text('Сколько вывести еще отелей:',
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=keyboards)
        bot.set_state(call.from_user.id, UserState.ask_send_add_inf_hotel, call.message.chat.id)
    else:
        bot.delete_message(call.message.chat.id, call.message.id)
        finish_work(call.from_user.id, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: bot.get_state(call.from_user.id, call.message.chat.id) ==
                            'UserState:ask_send_add_inf_hotel')
@logger.catch()
def callback_ask_send_add_inf_hotel(call: CallbackQuery) -> None:
    """Функция для обработки ответа пользователя при выборе количества вывода доп. отелей"""
    logger.info('Обработка ответа пользователя при ответе о выборе количества вывода доп. отелей')
    num_hotels = int(get_data(call.from_user.id, call.message.chat.id, 'num_hotels')) + int(call.data)
    set_data(call.from_user.id, call.message.chat.id, 'num_hotels', str(num_hotels))
    bot.delete_message(call.message.chat.id, call.message.id)
    start_send_hotel_inf(call.from_user.id, call.message.chat.id)


@bot.message_handler(state=UserState.ask_send_add_inf_hotel)
@logger.catch()
def error_confirm(message: Message) -> None:
    """Функция для оповещения пользователя о неверных действиях"""
    bot.send_message(message.chat.id, 'Выбор количества дополнительно выводимых отелей осуществляется только через '
                                      'кнопки в самом сообщении!\n'
                                      'Пожалуйста, нажмите на одну из кнопок в сообщении выше')
