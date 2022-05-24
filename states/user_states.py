from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    search_city = State()
    search_hotel = State()
    check_In = State()
    check_Out = State()
    quantity_hotels = State()
    # found_cities = State()
    # clarification_city = State()
    finish = State()
