'''Configurate Flask application'''
from app import environments
from datetime import timedelta


# Flask
SECRET_KEY = environments.SECRET_KEY
SESSION_COOKIE_NAME = 'QuizMeSession'
FLASK_DEBUG = 1

# Flask-Login
REMEMBER_COOKIE_DURATION = timedelta(days=30)