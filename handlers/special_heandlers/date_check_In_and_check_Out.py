from loader import bot
from states.user_states import UserState
from telegram_bot_calendar import DetailedTelegramCalendar
from telebot.types import CallbackQuery, Message
from utils.data import set_data, get_data
from keyboards.inline.keyboard_yes_or_no import keyboards_yes_or_no
from datetime import datetime, timedelta
from loguru import logger


@logger.catch()
def __choosing_actions__(user_id: int, chat_id: int) -> tuple:
    """Функция для выдачи слова и начальной даты для календаря в зависимости от состояния пользователя
    (для удобства написания кода)"""
    if bot.get_state(user_id, chat_id) == 'UserState:check_In':
        text = 'заезда'
        new_date = datetime.now().date()
    else:
        text = 'выезда'
        new_date = get_data(user_id, chat_id, 'check_In') + timedelta(days=1)
    return text, new_date


@logger.catch()
def start_calendar(user_id: int, chat_id: int) -> None:
    """Начало процедуры ввода даты"""
    bot.set_state(user_id, UserState.check_In, chat_id)
    start_input_data_in_calendar(user_id, chat_id)


@logger.catch()
def start_input_data_in_calendar(user_id: int, chat_id: int) -> None:
    """Функция для запуска календаря
    Сделана раздельно с началом процедуры ввода дат (start_calendar), т.к. используется несколько раз в разных
    состояниях (ввод въезда и выезда из отеля)"""
    text, my_date = __choosing_actions__(user_id, chat_id)
    calendar, step = DetailedTelegramCalendar(min_date=my_date, locale='ru').build()
    bot.send_message(user_id, f'Выберете дату {text}', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
@logger.catch()
def input_data_in_calendar(call: CallbackQuery) -> None:
    """Функция для продолжения работы календаря
    Запускается, при нажатии кнопок в календаре и завершает работе при выборе конечной даты"""
    text, my_date = __choosing_actions__(call.from_user.id, call.message.chat.id)
    result, key, step = DetailedTelegramCalendar(min_date=my_date, locale='ru').process(call.data)

    if not result and key:
        bot.edit_message_text(f'Выберете дату {text}',
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        set_data(call.from_user.id, call.message.chat.id, 'cache', result)
        # Отправка сообщения для подтверждения введенной даты
        bot.edit_message_text(f"Дата {text}: {result}. Верно?",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=keyboards_yes_or_no())


@bot.callback_query_handler(
    func=lambda call:
    bot.get_state(call.from_user.id, call.message.chat.id) in ('UserState:check_Out', 'UserState:check_In')
    )
@logger.catch()
def confirmation_date(call: CallbackQuery) -> None:
    """Функция для выполнения действий после подтверждения (или нет) даты"""
    from handlers.special_heandlers.quantity_hotels import start_quantity_hotels
    if call.data == 'Да':
        result = get_data(call.from_user.id, call.message.chat.id, 'cache')
        text = __choosing_actions__(call.from_user.id, call.message.chat.id)[0]
        bot.edit_message_text(f"Дата {text} {result}",
                              call.message.chat.id,
                              call.message.message_id)

        if bot.get_state(call.from_user.id, call.message.chat.id) == 'UserState:check_In':  # Если введена дата въезда
            set_data(call.from_user.id, call.message.chat.id, 'check_In', result)
            bot.set_state(call.from_user.id, UserState.check_Out, call.message.chat.id)
            start_input_data_in_calendar(call.from_user.id, call.message.chat.id)
        else:  # Если введена дата выезда
            set_data(call.from_user.id, call.message.chat.id, 'check_Out', result)
            start_quantity_hotels(call.from_user.id, call.message.chat.id)  # Запуск сценария ввода количества отелей
    else:  # Если пользователь не подтвердил дату (кнопка НЕТ), то запускаем заново ввод этой даты
        bot.delete_message(call.message.chat.id, call.message.id)
        start_calendar(call.from_user.id, call.message.chat.id)


@bot.message_handler(state=[UserState.check_In, UserState.check_Out])
@logger.catch()
def error_input_date(message: Message) -> None:
    """Функция для оповещения пользователя о неверных действиях"""
    bot.send_message(message.chat.id, 'При выборе даты, ввод осуществляется только через кнопки в самом сообщении!\n'
                                      'Пожалуйста, нажмите на кнопу сообщения выше')
