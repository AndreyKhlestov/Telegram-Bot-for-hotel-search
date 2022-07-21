from telebot.types import Message, ReplyKeyboardRemove
from states.user_states import UserState
from loader import bot
from utils.data import set_data
from keyboards.reply.default_reply_keyboard import reply_keyboards
from handlers.special_heandlers.price_max import start_price_max
from loguru import logger


@logger.catch()
def start_prise_min(user_id: int, chat_id: int) -> None:
    """Начало процедуры уточнения желаемой минимальной цены"""
    logger.info('Начало процедуры уточнения минимальной цены')
    bot.set_state(user_id, UserState.price_min, chat_id)
    bot.send_message(user_id, 'Введите желаемую минимальную цену (в рублях):',
                     reply_markup=reply_keyboards(['2000', '3000', '5000', '7000', '10000', '15000'], 3))


@bot.message_handler(state=UserState.price_min)
@logger.catch()
def set_price_min(message: Message) -> None:
    """Функция для проверки и сохранения минимальной цены"""
    logger.info('Проверка и сохранение минимальной цены')
    if message.text.isdigit():
        if int(message.text) > 0:
            set_data(message.from_user.id, message.chat.id, 'price_min', message.text)
            bot.send_message(message.from_user.id, 'Записал',
                             reply_markup=ReplyKeyboardRemove())
            start_price_max(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Цена отелей должна быть больше 0\n ')

    else:
        bot.send_message(message.from_user.id, 'Цена отелей должна быть целым числом\n ')
