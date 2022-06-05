from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    search_city = State()
    check_In = State()
    check_Out = State()
    ask_photo = State()
    quantity_hotels = State()
    confirm = State()
    quantity_photo = State()
    search_hotel = State()
    finish = State()
