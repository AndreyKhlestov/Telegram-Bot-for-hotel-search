from telebot.types import Message, InlineKeyboardMarkup, KeyboardButton, CallbackQuery, ReplyKeyboardMarkup


def reply_keyboards(data: list, columns: int = 1) -> ReplyKeyboardMarkup:
    keyboards = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(data), columns):
        buttons = data[i:i + columns]
        keyboards.add(*buttons)
    return keyboards
