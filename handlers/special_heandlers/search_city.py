from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from states.user_states import UserState
from loader import bot
from utils.request_to_api import request_to_api
from config_data import config
import re
import json


# @bot.message_handler()
def input_city(message: Message) -> None:
    bot.set_state(message.from_user.id, UserState.input_city, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите название города:')


@bot.message_handler(state=UserState.input_city)
def processing_city(message: Message) -> None:
    name_city = message.text
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": name_city, "locale": "en_US", "currency": "USD"}
    response = request_to_api(url, querystring)  # ответ на запрос

    # проверка в тексте ответа регулярным выражением (на случай, если не будет ключа)
    pattern = r'(?<="CITY_GROUP","entities":).+?[\]]'
    find = re.search(pattern, response.text)
    if find:

        data = json.loads(find[0])  # преобразуем в JSON формат
        if data:  # Если что-то нашел (результат поиска есть)
            # список имен городов, для будущего варианта выбора, если введенный город не совпадет с найденным
            name_cities_list = list()

            # словарь для городов, которые совпали с введенным пользователем (для случая, когда введенных города
            # может быть более одного), ключ - расположение (данные из "caption"), значение - 'destinationId'
            found_cities_dict = dict()
            for elem in data:
                # Проходим (проверяем) по всем вариантам ответа и собираем нужную информацию
                if elem["type"] == "CITY":
                    if elem["name"] == name_city:
                        # для случая, когда введенный город может быть более одного
                        pattern = r'(?<=</span>,).+'
                        find = re.search(pattern, elem["caption"])
                        found_cities_dict[elem['destinationId']] = name_city + ',' + find[0]

                    elif not elem["name"] in name_cities_list:
                        # список имен городов, для будущего варианта выбора, если введенный город не совпадет с
                        # найденным
                        name_cities_list.append(elem["name"])


            # Анализ вариантов ответа и действия на них
            if len(found_cities_dict) == 1:
                bot.send_message(message.from_user.id, f'Город {[i_key for i_key in found_cities_dict.keys()]} найден')
                bot.set_state(message.from_user.id, UserState.finish, message.chat.id)
                # TODO сделать запоминание id города
                # for i_key in found_cities_dict.keys():
                #     return i_key

            elif len(found_cities_dict) > 1:
                bot.send_message(message.from_user.id, 'Нашлось по вашему запросу более одного города.')
                destinations = InlineKeyboardMarkup()
                for i_key in found_cities_dict.keys():
                    destinations.add(InlineKeyboardButton(text=found_cities_dict[i_key], callback_data=i_key))
                bot.set_state(message.from_user.id, UserState.clarification_city, message.chat.id)
                bot.send_message(message.from_user.id, 'Пожалуйста, выберите из списка нужный вам город:',
                                 reply_markup=destinations)  # Отправляем кнопки с вариантами

            elif name_cities_list:  # если введенный город не совпадет с найденным
                destinations = InlineKeyboardMarkup()
                for i_name_city in name_cities_list:
                    destinations.add(InlineKeyboardButton(text=found_cities_dict[i_name_city],
                                                          callback_data=i_name_city))
                bot.send_message(message.from_user.id, 'Может вы имели город:',
                                 reply_markup=destinations)  # Отправляем кнопки с вариантами

                # TODO доделать
                # print('Может вы имели город: ', end='')
                # for i_name_city in name_cities_list:
                #     print(i_name_city, end=', ')
                # print()
                # return req_city()
            else:
                # Если в ответе не нашлось ни одного города, делаем рекурсию себя, пока не будет введен существующий
                # город

                bot.send_message(message.from_user.id, f'Город {name_city} не найден.')
                # TODO доделать
                # print('Город {name_city} не найден.'.format(
                #     name_city=name_city
                # ))
                # return req_city()

        else:  # Если поиск ничего не выдал, делаем рекурсию себя, пока не будет введен существующий город
            bot.send_message(message.from_user.id, f'Город {name_city} не найден.\nВведите правильное название города:')
    else:
        raise Exception('В ответе (на запрос "города") нет нужного ключа')


@bot.callback_query_handler(func=lambda call: True)
def processing_city(call: CallbackQuery) -> None:
    bot.send_message(call.message.chat.id, f'Перешел в состояние уточнения города. id {call.data}')
    bot.answer_callback_query(call.id)


@bot.message_handler(state=UserState.finish)
def processing_city(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Перешел в состояние поиска отеля')
