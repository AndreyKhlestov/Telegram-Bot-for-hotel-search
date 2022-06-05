from telebot.types import Message, InputMediaPhoto
from loader import bot
from utils.get_photo import get_photos


@bot.message_handler(commands=['test'])
def bot_start(message: Message):
    """Функция для тестирования работы бота"""
    pass
    # list_url_photo = get_photos("456130", '10')
    #
    # for i in range(1, len(list_url_photo) - 1):
    #     bot.send_media_group(message.chat.id, list_url_photo[:i])
    # bot.send_photo(message.chat.id, 'https://exp.cdn-hotels.com/hotels/9000000/8080000/8070700/8070610/62d4aa22_w.jpg')
    # bot.send_photo(message.chat.id, 'https://exp.cdn-hotels.com/hotels/9000000/8080000/8070700/8070610/de3ac78a_z.jpg')


