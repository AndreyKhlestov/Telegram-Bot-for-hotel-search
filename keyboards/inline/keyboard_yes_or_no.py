from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboards_yes_or_no(callback_data: list = None) -> InlineKeyboardMarkup:
    """inline клавиатура с кнопками 'Да' и 'Нет' """
    keyboards = InlineKeyboardMarkup()
    button_yes = InlineKeyboardButton(
        text='Да',
        callback_data='Да' if not callback_data else callback_data[0]
    )
    button_no = InlineKeyboardButton(
        text='Нет',
        callback_data='Нет' if not callback_data else callback_data[1]
    )
    keyboards.add(button_yes, button_no)
    return keyboards
