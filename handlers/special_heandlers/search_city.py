from telebot.types import Message
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
                # TODO сделать запоминание города
                # for i_key in found_cities_dict.keys():
                #     return i_key

            elif len(found_cities_dict) > 1:
                bot.send_message(message.from_user.id, 'Нашлось по вашему запросу более одного города.')
                bot.send_message(message.from_user.id, 'Пожалуйста, выберите из списка нужный вам город.')
                for i_value in found_cities_dict.values():
                    bot.send_message(message.from_user.id, i_value)
                bot.set_state(message.from_user.id, UserState.clarification_city, message.chat.id)
                # TODO доделать
                # print('Нашлось по вашему запросу более одного города.')
                # print('Пожалуйста, выберите из списка нужный вам город.')
                # for i_value in found_cities_dict.values():
                #     print(i_value)
                # caption = input()
                # for i_key in found_cities_dict.keys():
                #     if found_cities_dict[i_key] == caption:
                #         return i_key

            elif name_cities_list:  # если введенный город не совпадет с найденным
                bot.send_message(message.from_user.id, 'Может вы имели город:')
                for i_name_city in name_cities_list:
                    bot.send_message(message.from_user.id, i_name_city)
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
            bot.send_message(message.from_user.id, f'Город {name_city} не найден.')
            # TODO доделать
            # print('Город {name_city} не найден.'.format(
            #     name_city=name_city
            # ))
            # return req_city()
    else:
        raise Exception('В ответе (на запрос "города") нет нужного ключа')


@bot.message_handler(state=UserState.clarification_city)
def processing_city(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Перешел в состояние уточнения города')


@bot.message_handler(state=UserState.finish)
def processing_city(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Перешел в состояние поиска отеля')
