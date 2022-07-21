from telebot.types import Message
from loader import bot
from handlers.special_heandlers.search_city import start_search_city
from states.user_states import UserState
from utils.data import set_data
from loguru import logger


@bot.message_handler(commands=['lowprice'])
@logger.catch()
def bot_lowprice(message: Message):
    """Функция для запуска процедуры поиска дешевых отелей"""
    logger.info('Запущена команда "lowprice"')
    bot.set_state(message.from_user.id, UserState.start_command, message.chat.id)
    set_data(message.from_user.id, message.chat.id, 'commands', 'lowprice')
    start_search_city(message.from_user.id, message.chat.id)
