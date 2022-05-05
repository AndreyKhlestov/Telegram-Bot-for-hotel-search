import requests
import json
import os
import re
from dotenv import load_dotenv


def req_city():
    """
    Функция, реализующая запрос города через API и возвращающая ключ 'destinationId'
    """
    # Данные для запроса
    name_city = input('Введите название города: ')
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": name_city, "locale": "en_US", "currency": "USD"}
    load_dotenv()
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY')
    }

    # Парсим (используем таймаут(timeout) у запроса, чтобы не ждать продолжительное время ответа от сервера)
    response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)

    if response.status_code == requests.codes.ok:  # проверка статус кода ответа

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
                    for i_key in found_cities_dict.keys():
                        return i_key

                elif len(found_cities_dict) > 1:
                    print('Нашлось по вашему запросу более одного города.')
                    print('Пожалуйста, выберите из списка нужный вам город.')
                    for i_value in found_cities_dict.values():
                        print(i_value)
                    caption = input()
                    for i_key in found_cities_dict.keys():
                        if found_cities_dict[i_key] == caption:
                            return i_key

                elif name_cities_list:  # если введенный город не совпадет с найденным
                    print('Может вы имели город: ', end='')
                    for i_name_city in name_cities_list:
                        print(i_name_city, end=', ')
                    print()
                    return req_city()
                else:
                    # Если в ответе не нашлось ни одного города, делаем рекурсию себя, пока не будет введен существующий
                    # город
                    print('Город {name_city} не найден.'.format(
                        name_city=name_city
                    ))
                    return req_city()

            else:  # Если поиск ничего не выдал, делаем рекурсию себя, пока не будет введен существующий город
                print('Город {name_city} не найден.'.format(
                    name_city=name_city
                ))
                return req_city()
        else:
            raise Exception('В ответе (на запрос "города") нет нужного ключа')
    else:
        raise Exception('Статус код запроса "города" не положительный')
