from telebot.types import Message, ReplyKeyboardRemove
from states.user_states import UserState
from loader import bot
from utils.data import set_data, get_data
from keyboards.reply.default_reply_keyboard import reply_keyboards
from handlers.special_heandlers.min_distance import start_min_distance
from loguru import logger


@logger.catch()
def start_price_max(user_id: int, chat_id: int) -> None:
    """Начало процедуры уточнения желаемой максимальной цены"""
    bot.set_state(user_id, UserState.price_max, chat_id)
    min_price = int(get_data(user_id, chat_id, 'price_min'))
    list_num = [str(min_price + num*1000) for num in [1, 2, 3, 5, 7, 10]]
    bot.send_message(user_id, 'Введите желаемую максимальную цену (в рублях):',
                     reply_markup=reply_keyboards(list_num, 3))


@bot.message_handler(state=UserState.price_max)
@logger.catch()
def set_price_max(message: Message) -> None:
    """Функция для проверки и сохранения максимальной цены"""
    if message.text.isdigit():
        min_price = get_data(message.from_user.id, message.chat.id, 'price_min')

        if int(message.text) > int(min_price):
            set_data(message.from_user.id, message.chat.id, 'price_max', message.text)
            bot.send_message(message.from_user.id, 'Записал',
                             reply_markup=ReplyKeyboardRemove())
            start_min_distance(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Максимальная цена отелей должна быть больше минимальной\n ')

    else:
        bot.send_message(message.from_user.id, 'Цена отелей должна быть числом\n ')
