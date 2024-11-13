from flask import render_template, request, redirect, session, flash
from flask.views import MethodView
from controls import *


class AboutView(MethodView):
    """Класс представления страницы "О нас" """

    def get(self):
        """Метод обрабатывающий GET-запрос. Возвращает шаблон страницы about.html"""
        return render_template('about.html')


class RegistrationView(MethodView):
    """Класс представления страницы регистрации"""

    def get(self):
        """Метод обрабатывающий GET-запрос. Возвращает шаблон страницы registration.html"""
        return render_template('registration.html')

    def post(self):
        """Метод обрабатывающий POST-запрос. Обращается к БД и заносит данные пользователь (имя и пароль)"""
        data = request.form.to_dict()

        if 'login' not in data:

            if registration(data['name'], data['password'], session):
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
            res = login(data['name'], data['password'])
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

            if 'username' in session:
                user: Users = Users.get_or_none(name=session['username'])
                user_password = user.hash_password
                data = request.form.to_dict()
                site_name = data.pop('name')
                login = data.pop('login')
                length = int(data.pop('length'))
                choose = [i for i in data if
                          i in ["kiril_low", "kiril_up", "latin_low", "latin_up", "digits", "special"]]

                save_generated_password(user, user_password, site_name, login, length, choose)

                return render_template("password_generator.html", flag=True)
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
                user_name = session['username']
                user = Users.get_or_none(name=user_name)
                site_name = data['name']
                password = data['password']
                login = data['login']
                save_your_password(user, site_name, login, password)
                return render_template('your_password_input.html')
            else:
                return redirect('/login')
        else:
            return redirect('/your_passwords')


class YourPasswordView(MethodView):
    """Класс представления страницы с паролями пользователя"""

    def get(self):
        """Метод обрабатывающий GET-запрос. Возвращает шаблон страницы your_passwords.html"""

        if 'username' in session:
            passwords = show_passwords(session['username'])
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
