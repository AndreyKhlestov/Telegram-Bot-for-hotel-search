import telebot


bot = telebot.TeleBot("5350202476:AAFwlevujOZziIv-nPQ6KeETmBCs5PKD_sc")



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/Привет":
        bot.send_message(message.from_user.id, "И тебе привет.")
    elif message.text == "/help" or message.text == "/start":
        text = 'Поддерживаемые команды:\n' \
               '/lowprice - поиск самых дешёвых отелей в городе\n' \
               '/highprice - поиск самых дорогих отелей в городе\n' \
               '/bestdeal - поиск отелей, наиболее подходящих по цене и расположению от центра\n' \
               '/history - узнать историю поиска отелей'

        bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling()

telebot.TeleBot.set_my_commands()