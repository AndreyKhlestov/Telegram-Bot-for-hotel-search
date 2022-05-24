from telebot.types import Message, CallbackQuery
from states.user_states import UserState
from loader import bot
from utils.search_city import search_city
from handlers.special_heandlers.search_hotel import hotel_search


def start_search_city(message: Message) -> None:
    bot.set_state(message.from_user.id, UserState.search_city, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите название города:')


@bot.message_handler(state=UserState.search_city)
def processing_city(message: Message) -> None:
    search_city(message.text, message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def correction_city(call: CallbackQuery) -> None:
    bot.send_message(call.message.chat.id, f'Перешел в состояние уточнения города. id {call.data}')
    bot.answer_callback_query(call.id)  # отправка ответа на запрос (ничего не отправляет) - возможно не требуется
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['id_city'] = call.data
    hotel_search(call.from_user.id, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.isalpha())
def search_city_from_the_list(call: CallbackQuery) -> None:
    bot.send_message(call.message.chat.id, f'заново ищу город {call.data}')
    bot.answer_callback_query(call.id)  # отправка ответа на запрос (ничего не отправляет) - возможно не требуется
    search_city(call.data, call.from_user.id, call.message.chat.id)




