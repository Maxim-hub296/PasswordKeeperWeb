# Класс с представлениями страниц

from flask import render_template, request, redirect, session, flash  # Импортируем необходимое от фреймворка
from flask.views import MethodView  # Импортируем класс, от которого наследуемся
from controls import *  # Импортируем функции для представления


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
                flash('Такой пользователь уже есть')  # Возвращаем ошибку в модальный диалог
                return render_template('registration.html')  # Снова возвращаем шаблон регистрации
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
            res = login(data['name'], data['password'])  # Получаем True или False и соответственную ошибку
            if res[0]:
                session['username'] = data['name']  # Добавляем в сессию
                return redirect('/your_passwords')
            else:
                return render_template('login.html', message=res[1])
        if data.get('register', None):  # Если нажали кнопку регистрации
            return redirect("/registration")


class YourPasswordView(MethodView):
    """Класс представления страницы с паролями пользователя"""

    def get(self):
        """Метод обрабатывающий GET-запрос. Возвращает шаблон страницы your_passwords.html"""

        if 'username' in session:  # Если пользователь авторизован
            passwords = show_passwords(session['username'])  # Получаем список паролей и передаём в шаблон
            if passwords:
                return render_template('your_passwords.html', passwords=passwords)  # Если пароли есть - передаём
            else:
                return render_template("your_passwords.html",
                                       message="У вас нет паролей")  # Иначе передаём соответственный текст
        else:  # Иначе введем на авторизацию
            return redirect('/login')

    def post(self):
        """Метод обрабатывающий POST-запрос. Перенаправляет на страницу с паролями извне."""
        # Проверяем наличие ключей в форме и перенаправляем на нужные маршруты
        form_data = request.form.to_dict()
        if 'create' in form_data:
            return redirect('/password_generator')
        elif 'input' in form_data:
            return redirect('/your_password_input')

        # Если ни один ключ не найден, перенаправляем обратно на страницу паролей
        return redirect('/your_passwords')


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

            if 'username' in session:  # Если пользователь авторизирован, получаем данные, генерируем и сохраняем пароль
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
            else:  # Иначе введем авторизоваться
                return redirect('/login')
        if data.get('back', None) == 'back':  # Возвращаем к паролям при нажатии на соответствующую кнопку
            return redirect('/your_passwords')


class YourPasswordInputView(MethodView):
    """Класс представления ввода своего пароля"""

    def get(self):
        # Отображаем форму только если пользователь авторизован
        if "username" in session:
            return render_template('your_password_input.html', saved=False)
        else:
            return redirect('/login')

    def post(self):
        data = request.form.to_dict()

        # Проверка на наличие данных и авторизацию
        if "create" in data and 'username' in session:
            user_name = session['username']
            user = Users.get_or_none(name=user_name)

            # Если пользователь существует, сохраняем пароль
            if user:
                site_name = data['name']
                password = data['password']
                login = data['login']
                save_your_password(user, site_name, login, password)

                # Успешное сохранение, передаем `saved=True`
                return render_template('your_password_input.html', saved=True)
            else:
                # Если пользователь не найден, перенаправляем на страницу авторизации
                return redirect('/login')

        # Перенаправление на `/your_passwords` для всех прочих POST-запросов
        return redirect('/your_passwords')
