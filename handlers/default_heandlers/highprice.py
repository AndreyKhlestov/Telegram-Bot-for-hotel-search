from telebot.types import Message
from loader import bot
from handlers.special_heandlers.search_city import start_search_city
from states.user_states import UserState
from utils.data import set_data
from loguru import logger


@bot.message_handler(commands=['highprice'])
@logger.catch()
def bot_highprice(message: Message):
    """Функция для запуска процедуры поиска дорогих отелей"""
    logger.info('Запущена команда "highprice"')
    bot.set_state(message.from_user.id, UserState.start_command, message.chat.id)
    set_data(message.from_user.id, message.chat.id, 'commands', 'highprice')
    start_search_city(message.from_user.id, message.chat.id)
