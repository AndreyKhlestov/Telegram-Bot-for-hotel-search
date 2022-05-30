from loader import bot
from states.user_states import UserState
from telegram_bot_calendar import DetailedTelegramCalendar
from telebot.types import Message, CallbackQuery
from utils.data import set_data, get_data
from keyboards.inline.keyboard_yes_or_no import keyboards_yes_or_no
from datetime import datetime, timedelta
from keyboards.reply.default_reply_keyboard import reply_keyboards


def hotel_search(user_id: int, chat_id: int) -> None:
    """Начало процедуры поиска отеля"""
    bot.set_state(user_id, UserState.check_In, chat_id)
    start_calendar(user_id, chat_id)


def choosing_actions(user_id: int, chat_id: int) -> tuple:
    """Функция для выдачи слова и начальной даты для календаря в зависимости от состояния пользователя"""
    if bot.get_state(user_id, chat_id) == 'UserState:check_In':
        text = 'заезда'
        new_date = datetime.now().date()
    else:
        text = 'выезда'
        new_date = get_data(user_id, chat_id, 'check_In') + timedelta(days=1)
    return text, new_date


def start_calendar(user_id: int, chat_id: int):
    text, my_date = choosing_actions(user_id, chat_id)
    calendar, step = DetailedTelegramCalendar(min_date=my_date, locale='ru').build()
    bot.send_message(user_id, f'Выберете дату {text}', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def input_data_in_calendar(call: CallbackQuery) -> None:
    text, my_date = choosing_actions(call.from_user.id, call.message.chat.id)
    result, key, step = DetailedTelegramCalendar(min_date=my_date, locale='ru').process(call.data)

    if not result and key:
        bot.edit_message_text(f'Выберете дату {text}',
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        set_data(call.from_user.id, call.message.chat.id, 'cache', result)

        bot.edit_message_text(f"Дата {text}: {result}. Верно?",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=keyboards_yes_or_no())


@bot.callback_query_handler(
    func=lambda call:
    bot.get_state(call.from_user.id, call.message.chat.id) in ('UserState:check_Out', 'UserState:check_In')
    )
def confirmation_date(call: CallbackQuery) -> None:
    if call.data == 'Да':
        result = get_data(call.from_user.id, call.message.chat.id, 'cache')
        text = choosing_actions(call.from_user.id, call.message.chat.id)[0]
        bot.edit_message_text(f"Дата {text} {result}",
                              call.message.chat.id,
                              call.message.message_id)
        if bot.get_state(call.from_user.id, call.message.chat.id) == 'UserState:check_In':
            set_data(call.from_user.id, call.message.chat.id, 'check_In', result)
            bot.set_state(call.from_user.id, UserState.check_Out, call.message.chat.id)
            start_calendar(call.from_user.id, call.message.chat.id)
        else:
            set_data(call.from_user.id, call.message.chat.id, 'check_Out', result)
            bot.set_state(call.from_user.id, UserState.quantity_hotels, call.message.chat.id)
            start_quantity_hotels(call.from_user.id, call.message.chat.id)
    else:
        bot.delete_message(call.message.chat.id, call.message.id)
        start_calendar(call.from_user.id, call.message.chat.id)


def start_quantity_hotels(user_id: int, chat_id: int) -> None:
    bot.send_message(user_id, 'Введите количество отелей, которые необходимо вывести в результате (не больше 25)')


@bot.message_handler(state=UserState.quantity_hotels)
def quantity_hotels(message: Message) -> None:
    if message.text.isdigit():
        set_data(message.from_user.id, message.chat.id, 'num_hotels', message.text)

    else:
        bot.edit_message_text('Количество отелей должно быть числом\n '
                              'Введите количество отелей, которые необходимо вывести в результате (не больше 25)',
                              message.chat.id, message.message_id,
                              reply_markup=reply_keyboards([3, 5, 7, 10, 15, 20, 25]))

