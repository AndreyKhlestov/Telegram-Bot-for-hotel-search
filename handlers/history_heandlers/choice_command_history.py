from loader import bot
from loguru import logger
from database.models import HotelRequest
from states.user_states import UserState
from telebot.types import CallbackQuery
from keyboards.inline.default_inline_keyboards import inline_keyboards
from handlers.history_heandlers.send_history import send_history
from utils.data import set_data


@logger.catch()
def choice_command_history(user_id: int, chat_id: int) -> None:
    """Выдача списка команд для выбора поиска запроса из истории отелей"""
    logger.info('Выдача списка команд для выбора поиска запроса из истории отелей"')
    bot.set_state(user_id, UserState.choice_command_history, chat_id)

    sort_req = HotelRequest.select(HotelRequest.command).where(HotelRequest.user_id == user_id).distinct()

    commands = [i_req.command for i_req in sort_req]
    keyboards = inline_keyboards(commands)
    bot.send_message(user_id, 'Выдать историю запросов по команде:', reply_markup=keyboards)


@bot.callback_query_handler(func=lambda call: bot.get_state(call.from_user.id, call.message.chat.id) ==
                            'UserState:choice_command_history')
@logger.catch()
def callback_choice_command_history(call: CallbackQuery) -> None:
    """Функция для обработки ответа пользователя при выборе команды для поиска"""
    logger.info('Обработка ответа пользователя при выборе команды для поиска')
    bot.delete_message(call.message.chat.id, call.message.id)
    set_data(call.from_user.id, call.message.chat.id, 'commands', call.data)
    send_history(call.from_user.id, call.message.chat.id)
