from telebot.types import Message
from loguru import logger
from loader import bot


@bot.message_handler(state=None)
@logger.catch()
def bot_echo(message: Message):
    """Эхо хендлер, куда летят текстовые сообщения без указанного состояния"""
    bot.reply_to(message, f"{message.text} - неизвестная команда.\n"
                          f"Введите команду из меню или наберите /help")
