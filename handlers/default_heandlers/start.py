from telebot.types import Message
from loader import bot
from loguru import logger



@bot.message_handler(commands=['start'])
@logger.catch()
def bot_start(message: Message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")

