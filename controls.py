from database import Users, Passwords
from hashlib import sha256
from func import generate_password
from crypto import Crypto

def login(user: str, password: str) -> list[bool | str]:
    """Авторизация пользователя или возвращение ошибки"""
    user = Users.get_or_none(name=user)
    if user:

        if user.hash_password == sha256(password.encode()).hexdigest():
            return [True]
        else:

            return [False, "Неверный пароль"]
    else:
        return [False, "Неверное имя пользователя"]


def registration(name, password, session):
    if not Users.get_or_none(name=name):
        Users.get_or_create(name=name, hash_password=sha256(password.encode()).hexdigest())
        session["username"] = name
        return True
    else:
        return False


def save_generated_password(user: Users, user_password: str, site_name: str, login: str, length: int, choose: list):
    password = generate_password(length, choose)

    Passwords.get_or_create(user=user,
                            name_site=site_name,
                            login=login,
                            password=Crypto.encrypt(password, user_password))

def save_your_password(user, site_name, login, password):
    Passwords.get_or_create(user=user,
                            name_site=site_name,
                            login=login,
                            password=password)
    print("Пароль сохранен")

def show_passwords(user_name):
    user = Users.get_or_none(name=user_name)
    passwords = []
    for i in Passwords.select().where(Passwords.user == user):
        passwords.append(i)
    return passwords


