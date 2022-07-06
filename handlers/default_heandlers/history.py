from loader import bot
from loguru import logger
from telebot.types import Message
from handlers.history_heandlers.choice_history import choice_option_history


@bot.message_handler(commands=['history'])
@logger.catch()
def bot_history(message: Message):
    """Начало процедуры выдачи истории поиска отелей"""
    logger.info('Запущена команда "history"')
    choice_option_history(message)
