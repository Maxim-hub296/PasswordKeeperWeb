from flask import render_template, request, redirect, session, flash
from flask.views import MethodView
from database_manager import DataBaseManager
from func import generate_password
from crypto import Crypto


class AboutView(MethodView):
    """Класс представления страницы "О нас" """

    def get(self):
        """Метод обрабатывающий GET-запрос. Возвращает шаблон страницы about.html"""
        return render_template('about.html')

    def post(self):
        """Метод обрабатывающий POST-запрос. Направляет на страницы с регистрацией или авторизации.
        Использует шаблоны registration.html и login.html соответственно"""
        if 'register' in request.form.to_dict().keys():  # Проверка, какая кнопка была нажата
            # Если нажата кнопка "Зарегистрироваться"
            return redirect('/registration')
        else:
            # Если нажата кнопка "Авторизоваться"
            return redirect('/login')


class RegistrationView(MethodView):
    """Класс представления страницы регистрации"""

    def get(self):
        """Метод обрабатывающий GET-запрос. Возвращает шаблон страницы registration.html"""
        return render_template('registration.html')

    def post(self):
        """Метод обрабатывающий POST-запрос. Обращается к БД и заносит данные пользователь (имя и пароль)"""
        data = request.form.to_dict()
        print(data)
        if 'login' not in data:
            db = DataBaseManager()  # Инициализируем класс, тем самым обращаемся к БД
            print(data)
            if db.new_user(data['name'],
                           data['password']):  # Вносим и сохраняем нового пользователя

                session['username'] = data['name']

                return redirect('/your_passwords')  # Перенаправляем на страницу с паролями пользователя
            else:
                flash('Такой пользователь уже есть')
                return render_template('registration.html')
        else:
            return redirect('/login')


class LoginView(MethodView):
    """Класс представления страницы авторизации"""

    def get(self):
        """Метод обрабатывающий GET-запрос. Возвращает шаблон страницы login.html"""
        return render_template('login.html')

    def post(self):
        """Метод обрабатывающий POST-запрос. Обращается к БД и проверяет пароль и имя пользователя"""
        data = request.form.to_dict()

        if data.get('enter', None):
            db = DataBaseManager()
            res = db.login(data['name'], data['password'])
            print(res)
            if res[0]:
                session['username'] = data['name']
                return redirect('/your_passwords')
            else:
                return render_template('login.html', message=res[1])
        if data.get('register', None):
            return redirect("/registration")


class GeneratePassword(MethodView):
    """Класс представления страницы генерации пароля"""

    def get(self):
        """Метод обрабатывающий GET-запрос. Возвращает шаблон страницы password_generator.html
        Можно только авторизированным пользователям"""
        if 'username' in session:
            return render_template('password_generator.html')
        else:
            return redirect('/login')

    def post(self):
        """Метод обрабатывающий POST-запрос."""
        data = request.form.to_dict()
        if 'create' in data:
            del data['create']
            db = DataBaseManager()

            if 'username' in session:
                user_password = db.get_password_by_name(session['username'])
                data = request.form.to_dict()
                site_name = data.pop('name')
                length = int(data.pop('length'))
                choose = [i for i in data if
                          i in ["kiril_low", "kiril_up", "latin_low", "latin_up", "digits", "special"]]

                password = generate_password(length, choose)

                db.save_password(session['username'], site_name, Crypto.encrypt(password, user_password))

                return render_template("password_generator.html")
            else:
                return redirect('/login')
        if data.get('back', None) == 'back':
            return redirect('/your_passwords')


class YourPasswordInputView(MethodView):
    def get(self):
        if "username" in session:
            return render_template('your_password_input.html')
        else:
            return redirect('/login')

    def post(self):
        data = request.form.to_dict()
        if "create" in data:
            if 'username' in session:
                db = DataBaseManager()
                user_name = session['username']
                user_password = db.get_password_by_name(user_name)
                site_name = data['name']
                password = data['password']
                db.save_password(user_name, site_name, Crypto.encrypt(password, user_password))
                return render_template('your_password_input.html')
            else:
                return redirect('/login')
        else:
            return redirect('/your_passwords')


class YourPasswordView(MethodView):
    """Класс представления страницы с паролями пользователя"""

    def get(self):
        """Метод обрабатывающий GET-запрос. Возвращает шаблон страницы your_passwords.html"""
        db = DataBaseManager()

        if 'username' in session:
            passwords = db.get_user_passwords(session['username'])
            if passwords:
                return render_template('your_passwords.html', passwords=passwords)
            else:
                return render_template("your_passwords.html", message="У вас нет паролей")
        else:
            return redirect('/login')

    def post(self):
        if 'create' in request.form.to_dict().keys():
            return redirect('/password_generator')
        if 'input' in request.form.to_dict().keys():
            return redirect('/your_password_input')
