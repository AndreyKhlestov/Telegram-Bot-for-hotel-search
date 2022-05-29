from states.user_states import UserState
from loader import bot
from utils.request_to_api import request_to_api
import re
import json
from keyboards.inline.default_inline_keyboards import inline_keyboards
from handlers.special_heandlers.search_hotel import hotel_search


# def search_city(city: str, user_id: int, chat_id: int) -> tuple or None:
def search_city(city: str) -> tuple or None:
    name_city = city
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
            return found_cities_dict, name_cities_list

        #     # Анализ вариантов ответа и действия на них
        #     if len(found_cities_dict) == 1:  # Если нашелся только один вариант
        #         id_city = [i_key for i_key in found_cities_dict.keys()][0]
        #         bot.send_message(user_id, f'Город {id_city} найден')
        #         bot.set_state(user_id, UserState.finish, chat_id)
        #         with bot.retrieve_data(user_id, chat_id) as data:
        #             data['id_city'] = id_city
        #         hotel_search(user_id, chat_id)
        #
        #     elif len(found_cities_dict) > 1:
        #         bot.send_message(user_id, 'Нашлось по вашему запросу более одного города.')
        #         bot.send_message(user_id, 'Пожалуйста, выберите из списка нужный вам город:',
        #                          reply_markup=inline_keyboards(found_cities_dict))  # Отправляем кнопки с вариантами
        #
        #     else:
        #         bot.send_message(user_id, f'Город {name_city} не найден.')
        #         if name_cities_list:  # если есть похожие города
        #             bot.send_message(user_id, 'Может вы имели город:',
        #                              reply_markup=inline_keyboards(
        #                                  name_cities_list))  # Отправляем кнопки с возможными вариантами городов
        #
        # else:  # Если поиск ничего не выдал, делаем рекурсию себя, пока не будет введен существующий город
        #     bot.send_message(user_id, f'Город {name_city} не найден.\nВведите правильное название города:')
        else:
            return None
    else:
        raise Exception('В ответе (на запрос "города") нет нужного ключа')
