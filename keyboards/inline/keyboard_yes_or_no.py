from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboards_yes_or_no() -> InlineKeyboardMarkup:
    keyboards = InlineKeyboardMarkup()
    button_yes = InlineKeyboardButton(
        text='Да',
        callback_data='Да'
    )
    button_no = InlineKeyboardButton(
        text='Нет',
        callback_data='Нет'
    )
    keyboards.add(button_yes, button_no)
    return keyboards
