from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup


def inline_keyboards(data: list or dict) -> InlineKeyboardMarkup:
    keyboards = InlineKeyboardMarkup()
    for i_key in data:
        keyboards.add(InlineKeyboardButton(
            text=data[i_key] if isinstance(data, dict) else i_key,
            callback_data=i_key
        ))
    return keyboards
