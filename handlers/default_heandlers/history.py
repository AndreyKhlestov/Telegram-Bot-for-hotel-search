from telebot.types import Message
from loader import bot
from loguru import logger
from database.models import HotelRequest, Hotel
from handlers.special_heandlers.finish_work import finish_work
import time
from states.user_states import UserState
from telebot.types import Message, CallbackQuery
from keyboards.inline.keyboard_yes_or_no import keyboards_yes_or_no


@bot.message_handler(commands=['history'])
@logger.catch()
def bot_history(message: Message):
    """Начало процедуры выдачи истории поиска отелей"""
    logger.info('Запущена команда "history"')
    bot.set_state(message.from_user.id, UserState.history, message.chat.id)
    send_history(message.from_user.id, message.chat.id)


@logger.catch()
def send_history(user_id: int, chat_id: int, index: int = 0):
    """Отправка истории запроса отелей"""
    logger.info('Отправка истории запроса отелей')
    my_request = HotelRequest.select().where(HotelRequest.user_id == user_id)\
        .order_by(-HotelRequest.date)[index]

    text = f'🔍 Команда пользователя: {my_request.command}\n\n' \
           f'📅 Дата: {my_request.date.split()[0]}\n' \
           f'🕑 Время: {my_request.date.split()[1]}\n\n' \
           f'{my_request.main_info}'

    bot.send_message(user_id, text)

    hotels = Hotel.select().where(Hotel.request_id == my_request.id).order_by(Hotel.num_queue)
    for i_hotel in hotels:
        bot.send_message(user_id, i_hotel.hotel_info)
        time.sleep(1.1)

    if len(HotelRequest.select().where(HotelRequest.user_id == user_id)) - 1 == index:
        bot.send_message(user_id, '🛑 Запросов больше нет', )
        finish_work(user_id, chat_id)
    else:
        keyboards = keyboards_yes_or_no([str(index + 1), '0'])
        bot.send_message(user_id, 'Выдать предыдущий запрос?', reply_markup=keyboards)


@bot.callback_query_handler(func=lambda call:
                            bot.get_state(call.from_user.id, call.message.chat.id) == 'UserState:history')
@logger.catch()
def response_processing(call: CallbackQuery) -> None:
    """Функция для обработки ответа пользователя при вопросе о выдаче еще одного запроса"""
    logger.info('Обработка ответа пользователя при вопросе о выдаче еще одного запроса')

    bot.delete_message(call.message.chat.id, call.message.id)
    if call.data == '0':
        finish_work(call.from_user.id, call.message.chat.id)
    else:
        send_history(call.from_user.id, call.message.chat.id, int(call.data) + 1)


@bot.message_handler(state=UserState.history)
@logger.catch()
def error_input_date(message: Message) -> None:
    """Функция для оповещения пользователя о неверных действиях"""
    bot.send_message(message.chat.id, 'При работе с историей поиска отелей, ввод осуществляется только через кнопки в '
                                      'самом сообщении!\n'
                                      'Пожалуйста, нажмите на одну из кнопок в сообщении выше')
