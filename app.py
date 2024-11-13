# Настройки и запуск приложения
from flask import Flask  # Класс приложения
from views import AboutView, RegistrationView, YourPasswordView, LoginView, GeneratePassword, \
    YourPasswordInputView  # Классы представления
from secrets import token_hex  # Секретный ключ для сессии
from datetime import timedelta  # Для закрытия сессии через время
from database import *  # Для создания таблиц при запуске приложений

# Инициализируем все необходимое
app = Flask(__name__)

app.secret_key = token_hex(32)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# Добавляем пути соответственно нашим представлениям
app.add_url_rule('/', view_func=AboutView.as_view('about'))
app.add_url_rule('/registration', view_func=RegistrationView.as_view('registration'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/your_passwords', view_func=YourPasswordView.as_view('your_passwords'))
app.add_url_rule('/password_generator', view_func=GeneratePassword.as_view('password_generator'))
app.add_url_rule('/your_password_input', view_func=YourPasswordInputView.as_view('your_password_input'))

# Создаём таблицы (Если уже есть - ничего не произойдет)
create_tables()
# Запускаем приложение
app.run(debug=True)
