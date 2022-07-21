from loader import bot
from utils.data import get_data
from datetime import datetime, timedelta
from loguru import logger


@logger.catch()
def choosing_data(user_id: int, chat_id: int) -> tuple:
    """Функция для выдачи слова и начальной даты для календаря в зависимости от состояния пользователя
    (для удобства написания кода)"""
    if bot.get_state(user_id, chat_id) == 'UserState:check_In':
        text = 'заезда'
        new_date = datetime.now().date()
    else:
        text = 'выезда'
        new_date = get_data(user_id, chat_id, 'check_In') + timedelta(days=1)
    return text, new_date
