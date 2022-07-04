from loader import bot
from loguru import logger
from database.models import HotelRequest
from handlers.special_heandlers.finish_work import finish_work
from utils.data import set_data
from states.user_states import UserState
from telebot.types import Message, CallbackQuery
from keyboards.inline.default_inline_keyboards import inline_keyboards
from handlers.history_heandlers.send_history import send_history
from handlers.history_heandlers.search_location_history import search_location_history
from handlers.history_heandlers.choice_command_history import choice_command_history


@logger.catch()
def choice_option_history(message: Message) -> None:
    """Выдача вариантов для вывода истории запроса отелей"""
    logger.info('Выдача вариантов для вывода истории запроса отелей"')
    bot.set_state(message.from_user.id, UserState.choice_option_history, message.chat.id)

    # Обнуляем данные location и commands
    set_data(message.from_user.id, message.chat.id, 'location', '')
    set_data(message.from_user.id, message.chat.id, 'commands', '')

    requests = HotelRequest.select().where(HotelRequest.user_id == message.from_user.id)
    if requests:  # есть ли история запросов у пользователя
        commands = ['По дате', 'По локации', 'По команде для поиска']
        keyboards = inline_keyboards(commands)
        bot.send_message(message.from_user.id, 'Выдать историю запросов по:', reply_markup=keyboards)
    else:
        bot.send_message(message.from_user.id, 'Вы пока ничего не искали. История пуста')
        finish_work(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda call: bot.get_state(call.from_user.id, call.message.chat.id) ==
                            'UserState:choice_option_history')
@logger.catch()
def callback_choice_option_history(call: CallbackQuery) -> None:
    """Функция для обработки ответа пользователя при выборе метода для вывода истории"""
    logger.info('Обработка ответа пользователя при выборе метода для вывода истории')
    bot.delete_message(call.message.chat.id, call.message.id)
    if call.data == 'По дате':
        send_history(call.from_user.id, call.message.chat.id)
    elif call.data == 'По локации':
        search_location_history(call.from_user.id, call.message.chat.id)
    elif call.data == 'По команде для поиска':
        choice_command_history(call.from_user.id, call.message.chat.id)
