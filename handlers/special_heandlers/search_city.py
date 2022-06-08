from telebot.types import Message, CallbackQuery
from states.user_states import UserState
from loader import bot
from utils.search_city import search_city
from utils.data import set_data, get_data
from keyboards.inline.default_inline_keyboards import inline_keyboards
from handlers.special_heandlers.price_min import start_prise_min


def start_search_city(user_id: int, chat_id: int) -> None:
    """Начало процедуры поиска города"""
    bot.set_state(user_id, UserState.search_city, chat_id)
    bot.send_message(user_id, 'Введите название города:')


@bot.message_handler(state=UserState.search_city)
def processing_city(message: Message) -> None:
    """Функция для поиска города, введенного пользователем через клавиатуру"""
    name_city = message.text.capitalize()
    if search_city(name_city):
        found_cities_dict = search_city(name_city)
        keyboards = inline_keyboards(found_cities_dict)
        bot.send_message(message.from_user.id, 'Пожалуйста, выберите из списка нужный вам город или введите правильное '
                                               'название города (если его нет в списке)',
                         reply_markup=keyboards)  # Отправляем кнопки с вариантами
    else:  # Если поиск ничего не выдал
        bot.send_message(message.from_user.id, f'Город {name_city} не найден.\nВведите правильное название города:')


@bot.callback_query_handler(func=lambda call:
                            bot.get_state(call.from_user.id, call.message.chat.id) == 'UserState:search_city')
def correction_city(call: CallbackQuery) -> None:
    """
    Функция для выполнения действий после уточнения города (через Inline клавиатуру).
    При выборе города из найденных городов, ф-я получает id-города, сохраняет его и запускает сценарий поиска отелей
    """
    from handlers.special_heandlers.date_check_In_and_check_Out import start_calendar
    # Получаем название локации (города), который выбрал пользователь через кнопку
    for button in call.message.reply_markup.keyboard:
        if button[0].callback_data == call.data:
            location = button[0].text
            break

    bot.edit_message_text(f"Выбрано место: {location}",
                          call.message.chat.id,
                          call.message.message_id)
    set_data(call.from_user.id, call.message.chat.id, 'destination_Id', call.data)
    set_data(call.from_user.id, call.message.chat.id, 'location', location)
    if get_data(call.from_user.id, call.message.chat.id, 'commands') == 'bestdeal':
        start_prise_min(call.from_user.id, call.message.chat.id)
    else:
        start_calendar(call.from_user.id, call.message.chat.id)



