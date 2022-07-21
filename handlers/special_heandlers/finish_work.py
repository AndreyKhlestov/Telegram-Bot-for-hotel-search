from loguru import logger
from loader import bot
from states.user_states import UserState
from utils.data import set_data
from utils.data import get_data, set_data


@logger.catch()
def finish_work(user_id: int, chat_id: int) -> None:
    logger.info('Завершение выполнение команды')
    bot.set_state(user_id, UserState.finish, chat_id)

    # Обнуляем все переменные, которые использовали
    my_comand = get_data(user_id, chat_id, 'commands')

    if my_comand == 'bestdeal':
        set_data(user_id, chat_id, 'price_min', '')
        set_data(user_id, chat_id, 'price_max', '')
        set_data(user_id, chat_id, 'distance_min', '')
        set_data(user_id, chat_id, 'distance_max', '')

    set_data(user_id, chat_id, 'destination_Id', '')
    set_data(user_id, chat_id, 'cache', '')
    set_data(user_id, chat_id, 'check_In', '')
    set_data(user_id, chat_id, 'check_Out', '')
    set_data(user_id, chat_id, 'num_hotels', '')
    set_data(user_id, chat_id, 'main_info', '')
    set_data(user_id, chat_id, 'num_photo', '')
    set_data(user_id, chat_id, 'first_index_hotel', '')
    set_data(user_id, chat_id, 'pageNumber', '')
    set_data(user_id, chat_id, 'location', '')
    set_data(user_id, chat_id, 'commands', '')

    bot.send_message(user_id, 'Закончил выполнение команды')
