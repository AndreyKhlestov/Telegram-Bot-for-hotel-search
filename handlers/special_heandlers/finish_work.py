from loguru import logger
from loader import bot
from states.user_states import UserState


@logger.catch()
def finish_work(user_id: int, chat_id: int) -> None:
    bot.set_state(user_id, None, chat_id)
    bot.send_message(user_id, 'Введите команду из меню или наберите /help')
