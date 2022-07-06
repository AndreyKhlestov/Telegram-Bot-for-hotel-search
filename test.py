from loader import bot
from keyboards.inline.default_inline_keyboards import inline_keyboards


user_id = 465654693

locations = [
    'Паддингтон, Лондон Англия, Великоб-',
    'Лондон, Англия, Великобритания'
]
keyboards = inline_keyboards(locations)
bot.send_message(user_id, 'Выдать историю запросов по:', reply_markup=keyboards)

locations = dict()
for i_req in sort_req:
    locations[i_req.id_location] = i_req.location
keyboards = inline_keyboards(locations)
bot.send_message(user_id, 'Выдать историю запросов по:', reply_markup=keyboards)



# locations = [
#     'Паддингтон, Лондон, Англия, Великобритания',
#     'Варшава, Мазовецкое воеводство, Польша',
#     'Лондон, Англия, Великобритания'
# ]