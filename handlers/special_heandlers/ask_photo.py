from loader import bot
from states.user_states import UserState
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
from utils.data import set_data
from keyboards.inline.keyboard_yes_or_no import keyboards_yes_or_no
from keyboards.reply.default_reply_keyboard import reply_keyboards
from handlers.special_heandlers.send_inf_hotel import send_hotel_inf
from loguru import logger


@logger.catch()
def ask_photo(user_id: int, chat_id: int) -> None:
    """Начало процедуры вопроса о выводе фото отелей"""
    bot.set_state(user_id, UserState.ask_photo, chat_id)
    bot.send_message(user_id, f'Выводить фотографии отелей?',
                     reply_markup=keyboards_yes_or_no())


@bot.callback_query_handler(func=lambda call:
                            bot.get_state(call.from_user.id, call.message.chat.id) == 'UserState:ask_photo')
@logger.catch()
def confirmation_date(call: CallbackQuery) -> None:
    """Функция для обработки ответа пользователя (да/нет - через кнопку) на вопрос о выводе фото"""
    set_data(call.from_user.id, call.message.chat.id, 'print_photo', call.data)
    if call.data == 'Да':
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.from_user.id, 'Сколько выводить фотографий ? (не больше 10)',
                         reply_markup=reply_keyboards(['3', '5', '7', '10'], 2))
        bot.set_state(call.from_user.id, UserState.quantity_photo, call.message.chat.id)
    else:
        bot.edit_message_text('Вывод фотографий отключен',
                              call.message.chat.id,
                              call.message.message_id)
        send_hotel_inf(call.from_user.id, call.message.chat.id)


@bot.message_handler(state=UserState.quantity_photo)
@logger.catch()
def quantity_photo(message: Message) -> None:
    """Функция для выполнения действий после ввода пользователем количества фото"""
    if message.text.isdigit():
        if 0 < int(message.text) <= 10:
            set_data(message.from_user.id, message.chat.id, 'num_photo', message.text)
            bot.send_message(message.from_user.id, f'Включен вывод фотографий по {message.text} шт.',
                             reply_markup=ReplyKeyboardRemove())
            send_hotel_inf(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Количество фотографий должно быть больше 0 и не больше 10\n ')
    else:
        bot.send_message(message.from_user.id, 'Количество фотографий должно быть числом\n ')
