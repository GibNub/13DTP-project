"""init"""

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from prisma import register

from app.db import db
from app.user import AnonymousUser


# Base flask
app = Flask(__name__)
app.config.from_pyfile('config.py')


# Mail
mail = Mail()
mail.init_app(app)


# Database
register(db)


# Flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'account'
login_manager.login_message = 'Please log in to access this page'
login_manager.login_message_category = 'error'
login_manager.anonymous_user = AnonymousUser


from app import routes


app.run(debug=False)
