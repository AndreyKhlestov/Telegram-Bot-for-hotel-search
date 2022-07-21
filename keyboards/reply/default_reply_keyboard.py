from telebot.types import Message, InlineKeyboardMarkup, KeyboardButton, CallbackQuery, ReplyKeyboardMarkup


def reply_keyboards(data: list, columns: int = 1) -> ReplyKeyboardMarkup:
    """универсальная reply клавиатура
    Функция получает список, в котором находится текст для каждой кнопки, и количество столбцов (сколько будет кнопок
    в одной строке) и возвращает саму клавиатуру"""
    keyboards = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(data), columns):
        buttons = data[i:i + columns]
        keyboards.add(*buttons)
    return keyboards
