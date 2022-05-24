from loader import bot


def set_data(user_id: int, chat_id: int, key: str, value: str) -> None:
    with bot.retrieve_data(user_id, chat_id) as data:
        data[key] = value


def get_data(user_id: int, chat_id: int, key: str) -> str:
    with bot.retrieve_data(user_id, chat_id) as data:
        return data[key]
