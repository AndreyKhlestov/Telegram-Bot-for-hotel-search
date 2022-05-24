from loader import bot
from states.user_states import UserState
from telegram_bot_calendar import DetailedTelegramCalendar
from telebot.types import Message, CallbackQuery
from utils.data import set_data, get_data


def hotel_search(user_id: int, chat_id: int) -> None:
    bot.set_state(user_id, UserState.check_In, chat_id)
    start_calendar(user_id, chat_id)





def choosing_actions(user_id: int, chat_id: int) -> str:
    if bot.get_state(user_id, chat_id) == 'UserState:check_In':
        text = 'заезда'
    else:
        text = 'выезда'
    return text


def start_calendar(user_id: int, chat_id: int):
    text = choosing_actions(user_id, chat_id)
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(user_id, f'Выберете дату {text}', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def input_data_in_calendar(call: CallbackQuery):
    result, key, step = DetailedTelegramCalendar().process(call.data)
    if not result and key:
        text = choosing_actions(call.from_user.id, call.message.chat.id)
        bot.edit_message_text(f'Выберете дату {text}',
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали дату {result}",
                              call.message.chat.id,
                              call.message.message_id)
        if bot.get_state(call.from_user.id, call.message.chat.id) == 'UserState:check_In':
            set_data(call.from_user.id, call.message.chat.id, 'check_In', result)
            bot.set_state(call.from_user.id, UserState.check_Out, call.message.chat.id)
            start_calendar(call.from_user.id, call.message.chat.id)
        else:
            set_data(call.from_user.id, call.message.chat.id, 'check_Out', result)
            bot.set_state(call.from_user.id, UserState.quantity_hotels, call.message.chat.id)
            quantity_hotels(call.from_user.id, call.message.chat.id)


def quantity_hotels(user_id: int, chat_id: int) -> None:
    bot.send_message(user_id, f'Перешел в состояние ввода количества отелей {bot.get_state(user_id, chat_id)}')
