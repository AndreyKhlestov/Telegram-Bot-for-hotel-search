from loader import bot
from loguru import logger


@logger.catch()
def set_data(user_id: int, chat_id: int, key: str, value: str) -> None:
    """Функция для сохранения данных"""
    with bot.retrieve_data(user_id, chat_id) as data:
        data[key] = value


@logger.catch()
def get_data(user_id: int, chat_id: int, key: str) -> str or None:
    """Функция для вывода сохраненных данных"""
    try:
        with bot.retrieve_data(user_id, chat_id) as data:
            return data[key]
    except KeyError:
        return None
