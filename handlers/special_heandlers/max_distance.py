from telebot.types import Message, ReplyKeyboardRemove
from states.user_states import UserState
from loader import bot
from utils.data import set_data, get_data
from keyboards.reply.default_reply_keyboard import reply_keyboards
from handlers.special_heandlers.date_check_In_and_check_Out import start_calendar


def start_max_distance(user_id: int, chat_id: int) -> None:
    """Начало процедуры уточнения желаемого максимального расстояния от центра города"""
    bot.set_state(user_id, UserState.distance_max, chat_id)
    max_distance = int(get_data(user_id, chat_id, 'distance_min'))
    list_num = [max_distance + num for num in [1, 2, 3, 5, 7, 10]]
    bot.send_message(user_id, 'Введите желаемое максимальное расстояния от центра города (в км):',
                     reply_markup=reply_keyboards(list_num, 3))


@bot.message_handler(state=UserState.distance_max)
def set_max_distance(message: Message) -> None:
    """Функция для проверки и сохранения максимального расстояния от центра города"""
    if message.text.isdigit():
        if int(message.text) > int(get_data(message.from_user.id, message.chat.id, 'distance_min')):
            set_data(message.from_user.id, message.chat.id, 'distance_max', message.text)
            bot.send_message(message.from_user.id, 'Записал',
                             reply_markup=ReplyKeyboardRemove())
            start_calendar(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Расстояние до центра города должно быть больше минимального\n ')

    else:
        bot.send_message(message.from_user.id, 'Расстояние до центра города должно быть числом\n ')
