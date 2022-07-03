from telebot.types import Message
from loader import bot
from loguru import logger
from database.models import *
from handlers.special_heandlers.finish_work import finish_work
import time


@bot.message_handler(commands=['history'])
@logger.catch()
def bot_history(message: Message):
    logger.info('Запущена команда "history"')
    data = User.select().where(User.user_id == message.from_user.id)
    for i_data in data:
        bot.send_message(message.from_user.id, f'✍ Команда: {i_data.command}\n'
                                               f'📆 Дата: {i_data.date}\n'
                                               f'🕓 Время: {i_data.time}\n'
                                               f'📝 Найденные отели: \n{i_data.name_hotels}')
        time.sleep(1.1)
    finish_work(message.from_user.id, message.chat.id)
