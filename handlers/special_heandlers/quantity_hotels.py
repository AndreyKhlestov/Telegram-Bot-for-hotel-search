from loader import bot
from states.user_states import UserState
from telebot.types import Message, ReplyKeyboardRemove
from utils.data import set_data
from keyboards.reply.default_reply_keyboard import reply_keyboards


def start_quantity_hotels(user_id: int, chat_id: int) -> None:
    """Начало процедуры ввода количество отелей, которые необходимо вывести в результате"""
    bot.set_state(user_id, UserState.quantity_hotels, chat_id)
    bot.send_message(user_id, 'Введите количество отелей, которые необходимо вывести в результате (не больше 25)',
                              reply_markup=reply_keyboards(['5', '7', '10', '15', '20', '25'], 3))


@bot.message_handler(state=UserState.quantity_hotels)
def quantity_hotels(message: Message) -> None:
    """Функция для выполнения действий после ввода пользователя количества отелей"""
    from handlers.special_heandlers.confirm import confirm
    if message.text.isdigit():
        if 0 < int(message.text) <= 25:
            set_data(message.from_user.id, message.chat.id, 'num_hotels', message.text)
            bot.send_message(message.from_user.id, 'Записал',
                             reply_markup=ReplyKeyboardRemove())
            confirm(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Количество отелей должно быть больше 0 и не больше 25\n ')

    else:
        bot.send_message(message.from_user.id, 'Количество отелей должно быть числом\n ')
