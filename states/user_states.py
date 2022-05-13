from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    input_city = State()
    found_cities = State()
    clarification_city = State()
    finish = State()
