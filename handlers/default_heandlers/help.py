from telebot.types import Message
from loguru import logger
from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
@logger.catch()
def bot_help(message: Message):
    text = '\n'.join([f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS if command != 'help'])
    bot.send_message(message.from_user.id, f'Список команд:\n{text}')
