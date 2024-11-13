from peewee import MySQLDatabase, Model, CharField, PrimaryKeyField, ForeignKeyField
from crypto import Crypto

# Параметры подключения
db = MySQLDatabase(
    'database_test',  # Имя базы данных
    user='root',  # Имя пользователя
    password='maximwhite2008',  # Пароль
    host='127.0.0.1',  # Адрес хоста (например, localhost)
    port=3306  # Порт MySQL (по умолчанию 3306)
)


# Определите модель
class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    id = PrimaryKeyField()
    name = CharField(unique=True)
    hash_password = CharField()

    def __str__(self):
        return f'{self.name}'


class Passwords(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(Users, backref='passwords', on_delete='CASCADE')
    name_site = CharField()
    login = CharField()
    password = CharField()

    def __str__(self):
        return f"{self.name_site}: Логин - {self.login}, Пароль - {Crypto.decrypt(self.password, self.user.hash_password)}"


db.create_tables([Users, Passwords])


def create_tables():
    db.create_tables([Users, Passwords])

# db.drop_tables([Users, Passwords])  #!!!Убрать комментарий только если нужна пустая БД

# #
# for i in Users.select():
#     print(i)
#




# Passwords.get_or_create(user=Users.get_or_none(name="user1"),
#                         name_site="Google",
#                         login="log",
#                         password="qw34")

