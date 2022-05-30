from telebot.types import Message, InlineKeyboardMarkup, KeyboardButton, CallbackQuery, ReplyKeyboardMarkup


def reply_keyboards(data: list) -> ReplyKeyboardMarkup:
    keyboards = ReplyKeyboardMarkup()
    for i_key in data:
        keyboards.add(KeyboardButton(text=i_key))
    return keyboards
