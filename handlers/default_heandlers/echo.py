from telebot.types import Message
from loguru import logger
from loader import bot
from states.user_states import UserState


# @logger.catch()
# def start_echo(user_id: int, chat_id: int) -> None:
#     bot.set_state(user_id, None, chat_id)
#     bot.send_message(user_id, 'Введите команду из меню или наберите /help')


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
@logger.catch()
def bot_echo(message: Message):
    bot.reply_to(message, f"{message.text} - неизвестная команда.\n"
                          f"Введите команду из меню или наберите /help")
