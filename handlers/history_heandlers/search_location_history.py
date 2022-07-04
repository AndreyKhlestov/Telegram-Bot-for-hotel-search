from loader import bot
from loguru import logger
from database.models import HotelRequest
from states.user_states import UserState
from telebot.types import CallbackQuery
from keyboards.inline.default_inline_keyboards import inline_keyboards
from handlers.history_heandlers.send_history import send_history
from utils.data import set_data


@logger.catch()
def search_location_history(user_id: int, chat_id: int) -> None:
    """Выдача списка городов из истории запроса отелей"""
    logger.info('Выдача списка городов из истории запроса отелей"')
    bot.set_state(user_id, UserState.search_location_history, chat_id)

    sort_req = HotelRequest.select(HotelRequest.location).where(HotelRequest.user_id == user_id).distinct()

    locations = [i_req.location for i_req in sort_req]
    keyboards = inline_keyboards(locations)
    bot.send_message(user_id, 'Выдать историю запросов по:', reply_markup=keyboards)


@bot.callback_query_handler(func=lambda call: bot.get_state(call.from_user.id, call.message.chat.id) ==
                            'UserState:search_location_history')
@logger.catch()
def callback_search_location_history(call: CallbackQuery) -> None:
    """Функция для обработки ответа пользователя при выборе локации из истории"""
    logger.info('Обработка ответа пользователя при выборе метода локации из истории')
    bot.delete_message(call.message.chat.id, call.message.id)
    set_data(call.from_user.id, call.message.chat.id, 'location', call.data)
    send_history(call.from_user.id, call.message.chat.id)
