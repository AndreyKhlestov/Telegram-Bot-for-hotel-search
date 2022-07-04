from telebot.types import Message
from loguru import logger
from config_data.config import DEFAULT_COMMANDS
from loader import bot
from database.models import HotelRequest, Hotel
import json
import datetime
from keyboards.inline.keyboard_yes_or_no import keyboards_yes_or_no


@bot.message_handler(commands=['test'])
@logger.catch()
def bot_test(message: Message):
    bot.send_message(message.from_user.id, 'test')
    my_user_id = 465654693
    my_command = 'lowprice'
    my_location = 'Лондон, Англия, Великобритания'

    my_main_info = 'Выбрано место: Лондон, Англия, Великобритания\n' \
                    'Дата заезда: 2022-06-29\n' \
                    'Дата выезда: 2022-06-30\n' \
                    'Количество отелей для вывода : 5'

    my_inf_hotels = [
        (
            "🏨 Название отеля: Book a Bed Hostels\n\n"
            "⭐ Рейтинг: 6,4\n\n🗺 Адрес: 86 Tanner's Hill\n\n"
            "🚗 Расстояние до центра города: 7,9 км\n\n"
            "💵 Стоимость за ночь: 2006 руб\n\n"
            "💰 Общая стоимость: 2006 руб\n\n"
            "🌐 Ссылка: https://www.hotels.com/ho402789",
            402789
         ),
        (
            '🏨 Название отеля: Ibis Budget Heathrow Terminal 5\n\n'
            '⭐ Рейтинг: 8,2\n\n🗺 Адрес: Horton Road, Colnbrook\n\n'
            '🚗 Расстояние до центра города: 27 км\n\n'
            '💵 Стоимость за ночь: 2833 руб\n\n'
            '💰 Общая стоимость: 2833 руб\n\n'
            '🌐 Ссылка: https://www.hotels.com/ho2052638144',
            2052638144
        ),
        (
            '🏨 Название отеля: easyHotel London Croydon\n\n⭐ '
            'Рейтинг: 5,8\n\n🗺 Адрес: 22 Addiscombe Road\n\n'
            '🚗 Расстояние до центра города: 15 км\n\n'
            '💵 Стоимость за ночь: 2884 руб\n\n'
            '💰 Общая стоимость: 2884 руб\n\n'
            '🌐 Ссылка: https://www.hotels.com/ho711429824',
            711429824
        ),
        (
            '🏨 Название отеля: Heathrow Ensuites Rooms\n\n'
            '⭐ Рейтинг: 7,0\n\n🗺 Адрес: 215 Long Lane\n\n'
            '🚗 Расстояние до центра города: 24 км\n\n'
            '💵 Стоимость за ночь: 3014 руб\n\n'
            '💰 Общая стоимость: 3014 руб\n\n'
            '🌐 Ссылка: https://www.hotels.com/ho776585920',
            776585920
        ),
        (
            '🏨 Название отеля: The Hatton Rooms\n\n'
            '⭐ Рейтинг: 6,2\n\n'
            '🗺 Адрес: Hatton Rd\n\n'
            '🚗 Расстояние до центра города: 21 км\n\n'
            '💵 Стоимость за ночь: 3142 руб\n\n'
            '💰 Общая стоимость: 3142 руб\n\n'
            '🌐 Ссылка: https://www.hotels.com/ho1190457088',
            1190457088
        )
    ]

    index = 1
    location = 'Лондон, Англия,Великобритания'
    command = None
    text_button_yes = f'{index + 1},- {location},- {command}'
    keyboards = keyboards_yes_or_no([text_button_yes, 'exit'])
    bot.send_message(my_user_id, 'Выдать предыдущий запрос?', reply_markup=keyboards)

    # data = HotelRequest.select().where(HotelRequest.user_id == message.from_user.id).order_by(-HotelRequest.date)
    # for i_data in data:
    #     print(i_data.date)


    # data = HotelRequest.select().where(HotelRequest.user_id == my_user_id,
    #                                    (HotelRequest.command == my_command) |
    #                                    (HotelRequest.location == my_location)
    #                                    ).order_by(-HotelRequest.date)
    # for i_data in data:
    #     print(i_data.id, i_data.date)



