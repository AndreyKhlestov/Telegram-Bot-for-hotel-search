from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_keyboards(data: list or dict) -> InlineKeyboardMarkup:
    """Универсальная inline клавиатура
    Получает список или словарь и возвращает inline клавиатуру, в которой текст кнопок и возвращаемое значение берется
    из полученного списка или словаря"""
    keyboards = InlineKeyboardMarkup()
    for i_key in data:
        keyboards.add(InlineKeyboardButton(
            text=data[i_key] if isinstance(data, dict) else i_key,
            callback_data=i_key
        ))
    return keyboards
