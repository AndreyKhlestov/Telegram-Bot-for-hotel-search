from telebot.types import Message
from states.user_states import UserState
from loader import bot
from handlers.special_heandlers.search_city import input_city


@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: Message):
    input_city(message)
