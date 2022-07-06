
from database.models import Hotel


list_displayed_hotels = Hotel.select().where(Hotel.request_id == '27')
# list_displayed_hotels = Hotel.select().where(Hotel.request_id == '27').hotel_info
# my_list = [i_hotel.hotel_info for i_hotel in Hotel.select().where(Hotel.request_id == '27')]
list_id_hotels = [i_hotel.id for i_hotel in Hotel.select().where(Hotel.request_id == '27')]
print(list_id_hotels)
#
# @logger.catch()
# def start_send_hotel_inf(user_id: int, chat_id: int) -> None:
#     """Начало процедуры отправки информации об найденных отелях"""
#     logger.info('Начало процедуры отправки информации об найденных отелях')
#
#     # Сохраняем в базу о запросах и одновременно получаем id запроса
#     request_id = HotelRequest.create(user_id=user_id,
#                                      command=get_data(user_id, chat_id, 'commands'),
#                                      location=get_data(user_id, chat_id, 'location'),
#                                      main_info=get_data(user_id, chat_id, 'main_info'),
#                                      date=datetime.datetime.now().strftime('%Y.%m.%d  %H:%M:%S')
#                                      ).id
#
#     if get_data(user_id, chat_id, 'commands') == "bestdeal":
#         count_hotel = 0
#         page_number = 0
#         num_hotels = int(get_data(user_id, chat_id, 'num_hotels'))
#         pattern = r'(?<=Расстояние до центра города: ).+?(?= км)'
#         dis_min = int(get_data(user_id, chat_id, 'distance_min'))
#         dis_max = int(get_data(user_id, chat_id, 'distance_max'))
#
#         # Т.к. не все отели могут попасть в веденный пользователем промежуток расстояния до центра города, то считаем
#         # сколько отелей попало в промежуток, а если одного запроса не хватило, то запрашиваем следующую страницу отелей
#         while count_hotel < num_hotels:
#             page_number += 1
#             #Отправка текста и стикера поиска
#             message_with_stic = bot.send_message(user_id, 'Веду поиск отелей')
#             sticker = bot.send_sticker(chat_id,
#                                        'CAACAgIAAxkBAAEFJudiu0z--ent9HLJbsxM7S9nAQjK1QACIwADKA9qFCdRJeeMIKQGKQQ')
#
#             inf_hotels = search_hotel(user_id, chat_id, page_number)
#
#             # Удаление текста и стикера поиска
#             bot.delete_message(message_with_stic.chat.id, message_with_stic.id)
#             bot.delete_message(sticker.chat.id, sticker.id)
#
#             if inf_hotels:
#                 for text, id_hotel in inf_hotels:
#                     dis = float(re.search(pattern, text)[0].replace(',', '.'))  # получаем расстояние до центра города
#                     if dis_min <= dis <= dis_max:  # Если расстояние входит в промежуток введенный пользователем
#                         send_hotel_inf(user_id, chat_id, text, id_hotel)
#
#                         # Сохраняем в базу о найденных отелях
#                         Hotel.create(request_id=request_id,
#                                      num_queue=count_hotel,
#                                      hotel_info=text
#                                      )
#                         count_hotel += 1
#
#                         if count_hotel >= num_hotels:
#                             break
#                     if dis > dis_max:  # Если расстояние больше максимального
#                         num_hotels = count_hotel
#                         break
#             else:
#                 break
#
#         if 0 < count_hotel < int(get_data(user_id, chat_id, 'num_hotels')):
#             bot.send_message(user_id, '⚠ К сожалению, больше нет отелей подходящих по заданным критериям')
#         elif count_hotel == 0:
#             bot.send_message(user_id, '⚠ К сожалению, нет отелей подходящих по заданным критериям')
#
#     else:
#         # Отправка текста и стикера поиска
#         message_with_stic = bot.send_message(user_id, 'Веду поиск отелей')
#         sticker = bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEFJudiu0z--ent9HLJbsxM7S9nAQjK1QACIwADKA9qFCdRJeeMIKQGKQQ')
#
#         inf_hotels = search_hotel(user_id, chat_id)
#
#         # Удаление текста и стикера поиска
#         bot.delete_message(message_with_stic.chat.id, message_with_stic.id)
#         bot.delete_message(sticker.chat.id, sticker.id)
#
#         if inf_hotels:
#             for index, inf in enumerate(inf_hotels):
#                 text, id_hotel = inf
#                 send_hotel_inf(user_id, chat_id, text, id_hotel)
#
#                 # Сохраняем в базу о найденных отелях
#                 Hotel.create(request_id=request_id,
#                              num_queue=index,
#                              hotel_info=text
#                              )
#         else:
#             bot.send_message(user_id, '❌ К сожалению, нет отелей подходящих по заданным критериям')
#
#     #  Если в базу отелей не записали ни одной информации об отеле из нашего запроса,
#     #  то удаляем запрос из базы (запросов отелей) как ненужный
#     if len(Hotel.select().where(Hotel.request_id == request_id)) == 0:
#         HotelRequest.delete().where(HotelRequest.id == request_id).execute()
#
#     finish_work(user_id, chat_id)
