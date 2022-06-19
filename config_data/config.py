import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('help', 'Вывести справку'),
    ('lowprice', 'поиск самых дешёвых отелей в городе'),
    ('highprice', 'поиск самых дорогих отелей в городе'),
    ('bestdeal', 'поиск отелей, наиболее подходящих по цене и расположению от центра'),
    ('history', 'узнать историю поиска отелей')
)
# ('cd', 'прерывание выполнения команды и выход в меню')


LOCALE = "ru_RU"
CURRENCY = "RUB"

