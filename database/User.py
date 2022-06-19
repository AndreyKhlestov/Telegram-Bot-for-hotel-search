from peewee import *
import datetime

db = SqliteDatabase('database/database.db')


class User(Model):
    """Класс для работы с базой данных
    user_id - id пользователя
    command - команда пользователя
    time - время вывода информации
    date - дата вывода информации
    name_hotels - названия отелей, которые были выведены пользователю"""
    user_id = CharField()
    command = CharField()
    time = DateTimeField(default=datetime.datetime.now().strftime('%H:%M:%S'))
    date = DateField(default=datetime.datetime.now().strftime('%d.%m.%Y'))
    name_hotels = CharField()

    class Meta:
        database = db
