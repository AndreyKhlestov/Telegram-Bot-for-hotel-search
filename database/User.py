from peewee import *
import datetime

db = SqliteDatabase('database/database.db')


class User(Model):
    user_id = CharField()
    command = CharField()
    time = DateTimeField(default=datetime.datetime.now().strftime('%H:%M:%S'))
    date = DateField(default=datetime.datetime.now().strftime('%d.%m.%Y'))
    name_hotels = CharField()

    class Meta:
        database = db  # модель будет использовать базу данных 'people.db'
