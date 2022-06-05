from loader import bot
from states.user_states import UserState
from telebot.types import CallbackQuery
from utils.data import get_data
from keyboards.inline.keyboard_yes_or_no import keyboards_yes_or_no
import re


def confirm(user_id: int, chat_id: int) -> None:
    """Начало процедуры уточнения введенных данных пользователем"""
    bot.set_state(user_id, UserState.confirm, chat_id)
    bot.send_message(user_id, f'Верны ли данные?\n'
                              f'Выбрано место: {get_data(user_id, chat_id, "location")}\n'
                              f'Дата заезда: {get_data(user_id, chat_id, "check_In")}\n'
                              f'Дата выезда: {get_data(user_id, chat_id, "check_Out")}\n'
                              f'Количество отелей для вывода : {get_data(user_id, chat_id, "num_hotels")}\n',
                     reply_markup=keyboards_yes_or_no())


@bot.callback_query_handler(func=lambda call:
                            bot.get_state(call.from_user.id, call.message.chat.id) == 'UserState:confirm')
def confirmation_date(call: CallbackQuery) -> None:
    """Функция для обработки ответа пользователя (да/нет - через кнопку) при уточнении данных"""
    from handlers.special_heandlers.search_city import start_search_city
    from handlers.special_heandlers.ask_photo import ask_photo
    if call.data == 'Да':
        text = re.sub("Верны ли данные\?\n", '', call.message.text)
        bot.edit_message_text(text,
                              call.message.chat.id,
                              call.message.message_id)
        ask_photo(call.from_user.id, call.message.chat.id)
    else:
        start_search_city(call.from_user.id, call.message.chat.id)
