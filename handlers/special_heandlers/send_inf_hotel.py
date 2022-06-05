from loader import bot
from states.user_states import UserState
from utils.data import get_data
from utils.search_hotel import search_hotel
from utils.get_photo import get_photos


def send_hotel_inf(user_id: int, chat_id: int) -> None:
    """Функция для отправки информации об найденных отелях"""
    bot.send_message(user_id, 'Вот, что я нашел:')
    quantity_photo = get_data(user_id, chat_id, 'num_photo')  # Количество фото для вывода (str или None)
    for text, id_hotel in search_hotel(user_id, chat_id):
        if quantity_photo:
            list_url_photo = get_photos(id_hotel, quantity_photo)
            if int(quantity_photo) == 1:
                bot.send_photo(chat_id, list_url_photo[0])
            else:
                bot.send_media_group(chat_id, list_url_photo)
        bot.send_message(user_id, text)
    bot.set_state(user_id, UserState.finish, chat_id)
