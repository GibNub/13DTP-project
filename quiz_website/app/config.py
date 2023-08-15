'''Configurate Flask application'''
from app import environments
from datetime import timedelta


# Flask
SESSION_COOKIE_NAME = 'QuizMeSession'
SECRET_KEY = environments.SECRET_KEY
TOKEN_SALT = environments.TOKEN_SALT
FLASK_DEBUG = 1

# Flask-Login
REMEMBER_COOKIE_DURATION = timedelta(days=30)

# Flask-Mail
DEFAULT_MAIL_SENDER = 'noreplyquizmecomfirmation@gmail.com'
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'noreplyquizmecomfirmation@gmail.com'
MAIL_PASSWORD = environments.MAIL_PASSWORD
#