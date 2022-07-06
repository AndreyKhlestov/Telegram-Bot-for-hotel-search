from peewee import *

db = SqliteDatabase('database/database.db')


class BaseModel(Model):
    class Meta:
        database = db


class HotelRequest(BaseModel):
    """Класс для работы с базой данных, содержащей запросы пользователя
    id - индивидуальный номер запроса
    user_id - id пользователя
    command - команда пользователя
    location - название локации
    main_info - основная информация запроса
    date - дата и время вывода информации"""

    id = PrimaryKeyField(unique=True)
    user_id = CharField()
    command = CharField()
    id_location = CharField()
    location = CharField()
    main_info = CharField()
    date = DateTimeField()


class Hotel(BaseModel):
    """Класс для работы с базой данных, содержащей информацию об отелях

    request_id - индивидуальный номер запроса, к которому относится информация об отеле
    num_queue - номер вывода в очереди
    hotel_info - информация об отеле
    """
    request_id = ForeignKeyField(HotelRequest)
    hotel_id = CharField()
    num_queue = IntegerField()
    hotel_info = CharField()

