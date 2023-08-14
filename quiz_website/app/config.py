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
