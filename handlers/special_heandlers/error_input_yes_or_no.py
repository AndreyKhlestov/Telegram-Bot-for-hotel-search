from loader import bot
from states.user_states import UserState
from telebot.types import Message
from loguru import logger


@bot.message_handler(state=[UserState.ask_photo, UserState.confirm, UserState.send_inf_hotel])
@logger.catch()
def error_confirm(message: Message) -> None:
    """Функция для оповещения пользователя о неверных действиях при ожидании нажатия кнопок да или нет"""
    bot.send_message(message.chat.id, 'Подтверждение или отказ осуществляется только через кнопки'
                                      ' "Да" или "Нет" в самом сообщении!\n'
                                      'Пожалуйста, нажмите на кнопу сообщения выше')
