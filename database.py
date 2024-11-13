# ORM модели
from peewee import MySQLDatabase, Model, CharField, PrimaryKeyField, \
    ForeignKeyField  # Импорты полей и класса подключения к MySQL серверу
from crypto import Crypto  # Используется для __str__ метода в Passwords

# Параметры подключения
db = MySQLDatabase(
    '*****',  # Имя базы данных
    user='****',  # Имя пользователя
    password='****',  # Пароль
    host='****',  # Адрес хоста (например, localhost)
    port=3306  # Порт MySQL (по умолчанию 3306)
)


# Определите модель
class BaseModel(Model):
    """Базовая модель"""

    class Meta:
        database = db


class Users(BaseModel):
    """Модель таблицы с пользователями"""
    id = PrimaryKeyField()  # Поле id
    name = CharField(unique=True)  # Поле имя (имя уникальное)
    hash_password = CharField()  # Хэшированный пароль


class Passwords(BaseModel):
    """Модель таблицы с паролями"""
    id = PrimaryKeyField()  # Поле id
    user = ForeignKeyField(Users, backref='passwords',
                           on_delete='CASCADE')  # Поле пользователь из таблицы Users (при удаленье, пользователя удаляться и его пароли)
    name_site = CharField()  # Название сайта
    login = CharField()  # Логин к сайту
    password = CharField()  # Пароль к сайту

    def __str__(self):
        """Выводит данные о пароли (используется в передачи объекта в jinja)"""
        return f"{self.name_site}: Логин - {self.login}, Пароль - {Crypto.decrypt(self.password, self.user.hash_password)}"


def create_tables():
    """Создаём таблицы по моделям"""
    db.create_tables([Users, Passwords])

# db.drop_tables([Users, Passwords])  #!!!Убрать комментарий только если нужна пустая БД
