from telebot.types import Message
from loguru import logger
from loader import bot
from telebot.types import ReplyKeyboardRemove


@bot.message_handler(commands=['exit'])
@logger.catch()
def bot_exit(message: Message):
    from handlers.special_heandlers.finish_work import finish_work
    """Хэндлер для досрочного выхода из любой команды в любой момент"""
    logger.info('Досрочный выход из программы')
    state = bot.get_state(message.from_user.id, message.chat.id)
    if state is None or state == 'UserState:finish':
        bot.send_message(message.from_user.id, 'Никакая команда не запущена. Вы в основном меню')
    else:
        bot.delete_message(message.chat.id, message.id - 1)
        bot.send_message(message.from_user.id, 'Выход из сценария', reply_markup=ReplyKeyboardRemove())
        finish_work(message.from_user.id, message.chat.id)
