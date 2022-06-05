from telebot.types import Message
from states.user_states import UserState
from loader import bot
from handlers.special_heandlers.search_city import start_search_city


@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: Message):
    start_search_city(message.from_user.id, message.chat.id)
