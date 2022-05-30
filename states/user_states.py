from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    search_city = State()
    search_hotel = State()
    check_In = State()
    check_Out = State()
    quantity_hotels = State()
    finish = State()
