from telebot.types import Message, CallbackQuery
from states.user_states import UserState
from loader import bot
from utils.search_city import search_city
from handlers.special_heandlers.search_hotel import hotel_search
from utils.data import set_data
from keyboards.inline.default_inline_keyboards import inline_keyboards


def start_search_city(message: Message) -> None:
    """Начало процедуры поиска города"""
    bot.set_state(message.from_user.id, UserState.search_city, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите название города:')


@bot.message_handler(state=UserState.search_city)
def processing_city(message: Message) -> None:
    # TODO описание ф-ии
    name_city = message.text.capitalize()
    if search_city(name_city):
        found_cities_dict = search_city(name_city)
        keyboards = inline_keyboards(found_cities_dict)
        bot.send_message(message.from_user.id, 'Пожалуйста, выберите из списка нужный вам город:',
                         reply_markup=keyboards)  # Отправляем кнопки с вариантами
    else:  # Если поиск ничего не выдал
        bot.send_message(message.from_user.id, f'Город {name_city} не найден.\nВведите правильное название города:')


@bot.callback_query_handler(func=lambda call:
                            bot.get_state(call.from_user.id, call.message.chat.id) == 'UserState:search_city')
def correction_city(call: CallbackQuery) -> None:
    """
    Функция для выполнения действий после уточнения города.
    При выборе города из найденных городов, ф-я получает id-города, сохраняет его и запускает сценарий поиска отелей
    """
    for button in call.message.reply_markup.keyboard:
        if button[0].callback_data == call.data:
            location = button[0].text
            break
    bot.edit_message_text(f"Выбрано место: {location}",
                          call.message.chat.id,
                          call.message.message_id)
    set_data(call.from_user.id, call.message.chat.id, 'id_city', call.data)
    set_data(call.from_user.id, call.message.chat.id, 'location', location)
    hotel_search(call.from_user.id, call.message.chat.id)



