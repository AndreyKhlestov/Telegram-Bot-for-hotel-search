from telebot.types import Message
from loader import bot
from handlers.special_heandlers.search_city import start_search_city
from utils.data import set_data
from states.user_states import UserState
from loguru import logger


@bot.message_handler(commands=['bestdeal'])
@logger.catch()
def bot_bestdeal(message: Message):
    """Функция для запуска процедуры поиска дешевых отелей"""
    bot.set_state(message.from_user.id, UserState.start_command, message.chat.id)
    set_data(message.from_user.id, message.chat.id, 'commands', 'bestdeal')
    logger.info('Запущена команда "bestdeal"')
    start_search_city(message.from_user.id, message.chat.id)

