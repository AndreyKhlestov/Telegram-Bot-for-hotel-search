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
    found_cities_dict, name_cities_list = search_city(name_city)
    # Анализ вариантов ответа и действия на них
    if len(found_cities_dict) == 1:  # Если нашелся только один вариант
        id_city = [i_key for i_key in found_cities_dict.keys()][0]
        bot.send_message(message.from_user.id, f'Город {id_city} найден')
        bot.set_state(message.from_user.id, UserState.finish, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['id_city'] = id_city
        hotel_search(message.from_user.id, message.chat.id)

    elif len(found_cities_dict) > 1:
        bot.send_message(message.from_user.id, 'Нашлось по вашему запросу более одного города.')
        bot.send_message(message.from_user.id, 'Пожалуйста, выберите из списка нужный вам город:',
                         reply_markup=inline_keyboards(found_cities_dict))  # Отправляем кнопки с вариантами

    else:
        bot.send_message(message.from_user.id, f'Город {name_city} не найден.')
        if name_cities_list:  # если есть похожие города
            bot.send_message(message.from_user.id, 'Может вы имели город:',
                             reply_markup=inline_keyboards(
                                 name_cities_list))  # Отправляем кнопки с возможными вариантами городов

    # Если поиск ничего не выдал, делаем рекурсию себя, пока не будет введен существующий город
    bot.send_message(message.from_user.id, f'Город {name_city} не найден.\nВведите правильное название города:')


@bot.callback_query_handler(func=lambda call:
                            bot.get_state(call.from_user.id, call.message.chat.id) == 'UserState:search_city')
def correction_city(call: CallbackQuery) -> None:
    """
    Функция для выполнения действий после уточнения города.
    Если был выбор из найденных городов, то ф-я получает id-города, сохраняет id и запускает сценарий поиска отелей
    Иначе, если пользователь ошибся при вводе города, функция получает название нового города (через кнопку или ввод) и
    начинает поиск нового города
    """
    # TODO отправка сообщения о выбранном городе,
    #  Иначе функция получает название города через ввод?
    if call.data.isdigit():
        set_data(call.from_user.id, call.message.chat.id, 'id_city', call.data)
        hotel_search(call.from_user.id, call.message.chat.id)
    else:
        bot.send_message(call.message.chat.id, f'заново ищу город {call.data}')
        search_city(call.data, call.from_user.id, call.message.chat.id)




