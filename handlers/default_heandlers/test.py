from telebot.types import Message
from loader import bot
from utils.get_photo import get_photos
# from loguru import logger


@bot.message_handler(commands=['test'])
# @logger.catch()
def bot_test(message: Message):
    id_hotel = '1190457088'
    list_url_photo = get_photos(id_hotel, '10')
    bot.send_media_group(message.chat.id, list_url_photo)
    # for i in range(10):
    #     bot.send_photo(message.chat.id, list_url_photo[i].media)
    # url = 'https://exp.cdn-hotels.com/hotels/38000000/37180000/37170600/37170534/91350ae0_z.jpg'
    # url = 'https://exp.cdn-hotels.com/hotels/38000000/37180000/37170600/37170534/91350ae0_w.jpg'
    # bot.send_photo(message.chat.id, url)


