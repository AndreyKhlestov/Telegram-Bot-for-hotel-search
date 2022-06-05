import json
from config_data import config
from datetime import datetime, timedelta
import re


# text = "https://exp.cdn-hotels.com/hotels/37000000/36790000/36789900/36789845/29a6f0f3_{size}.jpg"
# url = re.sub("_{size}", '', text)
# print(url)



# def __import_date__(date: str):
#     date = date.split('-')
#     return datetime(int(date[0]), int(date[1]), int(date[2]))
#
#
# a = '2022-08-24'
# b = '2022-10-15'
# c = __import_date__(b) - __import_date__(a)
# print(c.days)




# def hotels():
#     with open('test.json', 'r') as file:
#         date = json.load(file)
#     for i_date in date:
#         i_hotel = dict()
#         i_hotel['name'] = i_date["name"]
#         i_hotel['address'] = i_date["address"]["streetAddress"]
#         i_hotel['distance'] = i_date["landmarks"][0]["distance"]
#         i_hotel['price'] = int(i_date["ratePlan"]["price"]["exactCurrent"])
#         i_hotel['id'] = i_date["id"]
#         yield i_hotel
#
#
# for i_hotel in hotels():
#     print(i_hotel)
#     # print()
#     # print(f'Название отеля: {i_date["name"]}')
#     # print(f'Адрес: {i_date["address"]["streetAddress"]}')
#     # print(f'Расстояние до центра города: {i_date["landmarks"][0]["distance"]}')
#     # print(f'Стоимость за ночь: {int(i_date["ratePlan"]["price"]["exactCurrent"])} руб')
#     # print(f'ID отеля: {i_date["id"]}')


# text = f'Название отеля: {i_data["name"]}\n' \
                #        f'Адрес: {i_data["address"]["streetAddress"]}\n' \
                #        f'Расстояние до центра города: {i_data["landmarks"][0]["distance"]}\n' \
                #        f'Стоимость за ночь: {int(i_data["ratePlan"]["price"]["exactCurrent"])}'
                #
                # id_hotel = i_data["id"]
                #
                #
                #
                # i_hotel = dict()
                # i_hotel['name'] = i_data["name"]
                # i_hotel['address'] = i_data["address"]["streetAddress"]
                # i_hotel['distance'] = i_data["landmarks"][0]["distance"]
                # i_hotel['price'] = int(i_data["ratePlan"]["price"]["exactCurrent"])
                # i_hotel['id'] = i_data["id"]
                # yield i_hotel


