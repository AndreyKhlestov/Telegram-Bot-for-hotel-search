from telebot.types import Message
from loguru import logger
from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
@logger.catch()
def bot_echo(message: Message):
    bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение:"
                          f"{message.text}")
