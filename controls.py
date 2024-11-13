# Функции для классов представления
from database import Users, Passwords  # Импортируем таблицы
from hashlib import sha256  # Для проверки пароля
from func import generate_password  # Для создания пароля
from crypto import Crypto  # Для шифровки/дешифровки пароля


def login(user: str, password: str) -> list[bool | str]:
    """Авторизация пользователя или возвращение ошибки"""
    user = Users.get_or_none(name=user)  # Получаем пользователя (имя, зашифрованный пароль)
    if user:  # Если такой пользователь есть
        if user.hash_password == sha256(
                password.encode()).hexdigest():  # Хэшируем пароль, что ввел пользователь и проверяем его с хэшем из БД
            return [True]  # Все хорошо, возвращаем True
        else:

            return [False, "Неверный пароль"]  # Возвращаем False и соответственную ошибку
    else:
        return [False, "Неверное имя пользователя"]  # Аналогично неверному паролю


def registration(name: str, password: str, session) -> bool:
    """Регистрирует пользователя, если пользователя с таким именем нет"""
    if not Users.get_or_none(name=name):  # Если пользователя с таким именем нет
        Users.get_or_create(name=name, hash_password=sha256(
            password.encode()).hexdigest())  # Создаём пользователя с именем и хэшируем пароль
        session["username"] = name  # Добавляем в сессию
        return True  # Все хорошо
    else:
        return False  # Пользователь с таким именем уже есть


def save_generated_password(user: Users, user_password: str, site_name: str, login: str, length: int,
                            choose: list) -> None:
    """Сохраняет пароль, сгенерированный на основе выбора пользователя"""
    password = generate_password(length, choose)  # Генерируем пароль с указанной длинной и выбранными чек боксами

    Passwords.get_or_create(user=user,
                            name_site=site_name,
                            login=login,
                            password=Crypto.encrypt(password,
                                                    user_password))  # Сохраняем пароль (здесь же шифруем) соответствующему пользователю, учитывая название сайта и введенный логин


def save_your_password(user: Users, site_name: str, login: str, password: str) -> None:
    """Сохраняет пароль, введенный пользователем"""
    Passwords.get_or_create(user=user,
                            name_site=site_name,
                            login=login,
                            password=Crypto.encrypt(password, user.hash_password))  # Аналогично предыдущей функции


def show_passwords(user_name: str) -> list:
    """Возвращает все пароли пользователя"""
    user = Users.get_or_none(name=user_name)  # Получаем пользователя (объект)
    passwords = []  # Инициализируем список
    for i in Passwords.select().where(Passwords.user == user):  # Пробегаемся по паролям и добавляем
        passwords.append(i)
    return passwords  # Возвращаем список паролей (в последствии передаём в шаблон)
