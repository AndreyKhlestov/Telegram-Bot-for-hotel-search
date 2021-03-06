from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):  # Состояния пользователя
    start_command = State()
    search_city = State()
    price_min = State()
    price_max = State()
    distance_min = State()
    distance_max = State()
    check_In = State()
    check_Out = State()
    ask_photo = State()
    quantity_hotels = State()
    confirm = State()
    quantity_photo = State()
    search_hotel = State()
    send_inf_hotel = State()
    ask_send_add_inf_hotel = State()
    finish = State()

    choice_option_history = State()
    send_history = State()
    search_location_history = State()
    choice_command_history = State()
