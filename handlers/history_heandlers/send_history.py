from loader import bot
from loguru import logger
from database.models import HotelRequest, Hotel
from handlers.special_heandlers.finish_work import finish_work
import time
from states.user_states import UserState
from telebot.types import CallbackQuery
from keyboards.inline.keyboard_yes_or_no import keyboards_yes_or_no
from utils.data import get_data


@logger.catch()
def send_history(user_id: int, chat_id: int, index: int = 0):
    """Отправка истории запроса отелей"""
    logger.info('Отправка истории запроса отелей')

    bot.set_state(user_id, UserState.send_history, chat_id)

    location = get_data(user_id, chat_id, "location")
    command = get_data(user_id, chat_id, 'commands')

    if location:
        requests = HotelRequest.select().where(HotelRequest.user_id == user_id, HotelRequest.id_location == location) \
                        .order_by(-HotelRequest.date)

    elif command:
        requests = HotelRequest.select().where(HotelRequest.user_id == user_id, HotelRequest.command == command) \
            .order_by(-HotelRequest.date)
    else:
        requests = HotelRequest.select().where(HotelRequest.user_id == user_id).order_by(-HotelRequest.date)
    my_request = requests[index]
    limit_req = len(requests)

    text = f'🔍 Команда пользователя: {my_request.command}\n\n' \
           f'📅 Дата: {my_request.date.split()[0]}\n' \
           f'🕑 Время: {my_request.date.split()[1]}\n\n' \
           f'{my_request.main_info}'

    bot.send_message(user_id, text)

    hotels = Hotel.select().where(Hotel.request_id == my_request.id).order_by(Hotel.num_queue)
    for i_hotel in hotels:
        bot.send_message(user_id, i_hotel.hotel_info)
        time.sleep(1.1)

    if limit_req == index + 1:
        bot.send_message(user_id, '🛑 Запросов больше нет', )
        finish_work(user_id, chat_id)
    else:
        keyboards = keyboards_yes_or_no([str(index + 1), 'exit'])
        bot.send_message(user_id, 'Выдать предыдущий запрос?', reply_markup=keyboards)


@bot.callback_query_handler(func=lambda call:
                            bot.get_state(call.from_user.id, call.message.chat.id) == 'UserState:send_history')
@logger.catch()
def response_processing(call: CallbackQuery) -> None:
    """Функция для обработки ответа пользователя при вопросе о выдаче еще одного запроса"""
    logger.info('Обработка ответа пользователя при вопросе о выдаче еще одного запроса')

    bot.delete_message(call.message.chat.id, call.message.id)
    if call.data == 'exit':
        finish_work(call.from_user.id, call.message.chat.id)
    else:
        send_history(call.from_user.id, call.message.chat.id, index=int(call.data))
