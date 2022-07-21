from loader import bot
from loguru import logger
from states.user_states import UserState
from telebot.types import Message


@bot.message_handler(state=[UserState.choice_command_history,
                            UserState.choice_option_history,
                            UserState.search_location_history,
                            UserState.send_history
                            ])
@logger.catch()
def error_input_date(message: Message) -> None:
    """Функция для оповещения пользователя о неверных действиях"""
    bot.send_message(message.chat.id, 'При работе с историей поиска отелей, ввод осуществляется только через кнопки в '
                                      'самом сообщении!\n'
                                      'Пожалуйста, нажмите на одну из кнопок в сообщении выше')
