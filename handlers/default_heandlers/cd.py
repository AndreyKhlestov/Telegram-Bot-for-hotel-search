# from telebot.types import Message
# from loguru import logger
# from loader import bot
# from states.user_states import UserState
# from handlers.special_heandlers.finish_work import finish_work
#
#
# # @bot.message_handler(state=[UserState.search_city, UserState.price_min], commands=['cd'])
# # @bot.message_handler(state=UserState.search_city)
# @bot.message_handler(commands=['cd'])
# @logger.catch()
# def bot_cd(message: Message):
#     finish_work(message.from_user.id, message.chat.id)
