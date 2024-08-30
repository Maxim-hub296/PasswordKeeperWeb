from flask import Flask
from views import AboutView, RegistrationView, YourPasswordView, LoginView, GeneratePassword, YourPasswordInputView
from secrets import token_hex
from datetime import timedelta

app = Flask(__name__)

app.secret_key = token_hex(32)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

app.add_url_rule('/', view_func=AboutView.as_view('about'))
app.add_url_rule('/registration', view_func=RegistrationView.as_view('registration'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/your_passwords', view_func=YourPasswordView.as_view('your_passwords'))
app.add_url_rule('/password_generator', view_func=GeneratePassword.as_view('password_generator'))
app.add_url_rule('/your_password_input', view_func=YourPasswordInputView.as_view('your_password_input'))

app.run(debug=True)
