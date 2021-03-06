from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from loguru import logger
from database.models import db, HotelRequest, Hotel


if __name__ == '__main__':
    # Настройка логирования в файл
    logger.add('logs.log', level='DEBUG', format='{time} {level} {message}', rotation='250 MB', compression='zip')

    with db:
        db.create_tables([HotelRequest, Hotel])

    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    logger.info('Бот запущен')
    bot.infinity_polling()
