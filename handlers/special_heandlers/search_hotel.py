# import handlers.special_heandlers.date_check_In_and_check_Out
# from loader import bot
# from states.user_states import UserState
# from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
# from utils.request_to_api import request_to_api
# from utils.data import set_data, get_data
# from keyboards.inline.keyboard_yes_or_no import keyboards_yes_or_no
# from keyboards.reply.default_reply_keyboard import reply_keyboards
# from config_data import config
# import re
# from utils.search_hotel import search_hotel
# import json
#
#
# # def start_hotel_search(user_id: int, chat_id: int) -> None:
# #     """Начало процедуры поиска отеля"""
# #     from handlers.special_heandlers.date_check_In_and_check_Out import start_calendar
# #     bot.set_state(user_id, UserState.check_In, chat_id)
# #     start_calendar(user_id, chat_id)
#
# def print_hotel_inf_(user_id: int, chat_id: int) -> None:
#     """Начало процедуры поиска отеля"""
#     bot.send_message(user_id, 'Вот, что я нашел: ', reply_markup=ReplyKeyboardRemove())
#     for text, id_hotel in search_hotel(user_id, chat_id):
#         bot.send_message(user_id, text)
#     bot.set_state(user_id, UserState.search_hotel, chat_id)




