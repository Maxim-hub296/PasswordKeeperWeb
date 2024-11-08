import sqlite3
from db_commands import *
from hashlib import sha256
from crypto import Crypto


class DataBaseManager:
    def __init__(self) -> None:
        """Инициализируем все, что нужно и создаём/проверяем таблицы"""
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute(create_users_passwords_table)
        self.cursor.execute(create_users_table)
        self.cursor.execute(create_site_passwords_table)

    def new_user(self, user: str, password: str) -> bool:
        """Добавляем нового пользователя в базу данных"""
        if not self.user_exists(user):
            try:

                api_key = sha256(user.encode()).hexdigest()

                self.cursor.execute(
                    insert_user_and_password,
                    (user, sha256(password.encode()).hexdigest()),
                )
                self.cursor.execute(
                    insert_user,
                    (
                        user,
                        api_key,
                    ),
                )
                self.conn.commit()
                return True

            except sqlite3.IntegrityError:
                pass

        else:
            return False

    def user_exists(self, user: str) -> bool:
        """Проверяет существование пользователь"""
        self.cursor.execute(get_users)
        users = [row[0] for row in self.cursor.fetchall()]
        return user in users

    def login(self, user: str, password: str) -> list[bool | str]:
        """Авторизация пользователя или возвращение ошибки"""
        if self.user_exists(user):
            self.cursor.execute(get_password_by_name, (user,))
            result = self.cursor.fetchone()
            if result and sha256(password.encode()).hexdigest() == result[0]:
                return [True]
            else:
                return [False, "Неверный пароль"]
        else:
            return [False, "Неверное имя пользователя"]

    def save_password(self, user: str, site_name: str, password: str) -> None:
        """Сохраняет пароль дял сайта в базу данных"""
        self.cursor.execute(insert_site_passwords, (user, site_name, password))
        self.conn.commit()

    def get_password_by_name(self, user_name: str) -> str:
        """Получить пароль по имени пользователя"""
        self.cursor.execute(get_password_by_name, (user_name,))
        password = self.cursor.fetchone()
        return password[0]

    def get_user_passwords(self, user: str) -> list[str]:
        """Получить все пароли пользователя"""
        self.cursor.execute(get_user_passwords, (user,))
        rows = self.cursor.fetchall()
        user_password = self.get_password_by_name(user)
        passwords = []
        for row in rows:
            password_line = f"{row[0]} - {Crypto.decrypt(row[1], user_password)}"
            passwords.append(password_line)
        return passwords


class ApiDatabaseManager:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()

    def get_password_by_name(self, user_name: str) -> str:
        """Получить пароль по имени пользователя"""
        self.cursor.execute(get_password_by_name, (user_name,))
        password = self.cursor.fetchone()
        return password[0]

    def get_user_passwords_api(self, api_key: str) -> dict[str, str]:
        """Получить все пароли пользователя через API-ключ"""
        self.cursor.execute(get_username_api, (api_key,))
        user_name = self.cursor.fetchone()
        if user_name:
            user_name = user_name[0]
            self.cursor.execute(get_user_passwords, (user_name,))
            rows = self.cursor.fetchall()
            user_password = self.get_password_by_name(user_name)
            passwords = {}
            for row in rows:
                passwords[row[0]] = Crypto.decrypt(row[1], user_password)
            return passwords
        else:
            return {"error": "Invalid API key or user not found"}
