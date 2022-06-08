from telebot.types import Message
from loader import bot
from handlers.special_heandlers.search_city import start_search_city
from utils.data import set_data


@bot.message_handler(commands=['bestdeal'])
def bot_bestdeal(message: Message):
    """Функция для запуска процедуры поиска дешевых отелей"""
    set_data(message.from_user.id, message.chat.id, 'commands', 'bestdeal')
    start_search_city(message.from_user.id, message.chat.id)
