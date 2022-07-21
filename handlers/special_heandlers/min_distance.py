from telebot.types import Message, ReplyKeyboardRemove
from states.user_states import UserState
from loader import bot
from utils.data import set_data
from keyboards.reply.default_reply_keyboard import reply_keyboards
from handlers.special_heandlers.max_distance import start_max_distance
from loguru import logger


@logger.catch()
def start_min_distance(user_id: int, chat_id: int) -> None:
    """Начало процедуры уточнения желаемого минимального расстояния от центра города"""
    logger.info('Начало процедуры уточнения минимального расстояния от центра города')
    bot.set_state(user_id, UserState.distance_min, chat_id)
    bot.send_message(user_id, 'Введите желаемое минимальное расстояния от центра города (в км):',
                     reply_markup=reply_keyboards(['1', '2', '3', '5', '7', '10'], 3))


@bot.message_handler(state=UserState.distance_min)
@logger.catch()
def set_min_distance(message: Message) -> None:
    """Функция для проверки и сохранения минимального расстояния от центра города"""
    logger.info('Проверка и сохранение минимального расстояния от центра города')
    if message.text.isdigit():
        if int(message.text) > 0:
            set_data(message.from_user.id, message.chat.id, 'distance_min', message.text)
            bot.send_message(message.from_user.id, 'Записал',
                             reply_markup=ReplyKeyboardRemove())
            start_max_distance(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Расстояние до центра города должно быть больше 0\n ')

    else:
        bot.send_message(message.from_user.id, 'Расстояние до центра города должно быть целым числом\n ')

