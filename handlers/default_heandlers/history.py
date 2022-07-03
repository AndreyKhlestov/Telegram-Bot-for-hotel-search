from telebot.types import Message
from loader import bot
from loguru import logger
from database.models import HotelRequest, Hotel
from handlers.special_heandlers.finish_work import finish_work
import time


@bot.message_handler(commands=['history'])
@logger.catch()
def bot_history(message: Message):
    logger.info('Запущена команда "history"')

    # Вывод последнего запроса
    my_request = HotelRequest.select().where(HotelRequest.user_id == message.from_user.id).order_by(-HotelRequest.date)\
        .get()
    text = f'🔍 Команда пользователя: {my_request.command}\n\n' \
           f'📅 Дата: {my_request.date.split()[0]}\n' \
           f'🕑 Время: {my_request.date.split()[1]}\n\n' \
           f'{my_request.main_info}'

    bot.send_message(message.from_user.id, text)

    hotels = Hotel.select().where(Hotel.request_id == my_request.id).order_by(Hotel.num_queue)
    for i_hotel in hotels:
        bot.send_message(message.from_user.id, i_hotel.hotel_info)
        time.sleep(1.1)
    finish_work(message.from_user.id, message.chat.id)
