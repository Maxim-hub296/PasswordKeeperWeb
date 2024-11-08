# Команда для создания таблице users_passwords
create_users_passwords_table = """
        CREATE TABLE IF NOT EXISTS user_passwords (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
        """

# Команда для создания таблицы users
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
)
"""

# Команда для создания таблицы site_passwords
create_site_passwords_table = """
CREATE TABLE IF NOT EXISTS site_passwords (
    username TEXT,
    site TEXT,
    password TEXT,
    PRIMARY KEY (username, site),
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
)
"""
insert_user_and_password = "INSERT INTO user_passwords (username, password) VALUES (?, ?)"  # Не забывай передавать
# имя и пароль

# Команда для вставки пользователя в таблицу users
insert_user = """
INSERT INTO users (username) VALUES (?)
"""

# Команда для вставки паролей для сайтов в таблицу site_passwords
insert_site_passwords = """
INSERT INTO site_passwords (username, site, password)
VALUES (?, ?, ?) 
"""  # передавать имя пользователя, название сайта, пароль для сайта

get_password_by_name = "SELECT password FROM user_passwords WHERE username = ?"  # Не забывай передавать имя!

exists_user = (
    "SELECT 1 FROM user_passwords WHERE username = ?"  # Не забывай передавать имя
)

get_user_passwords = "SELECT site, password FROM site_passwords WHERE username = ?"

get_users = "SELECT * FROM users"
