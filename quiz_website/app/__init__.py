"""init"""

from flask import Flask
from flask_login import LoginManager
from prisma import register

from app.db import db
from app.user import AnonymousUser


# Base flask
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Database
register(db)

# Flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'account'
login_manager.anonymous_user = AnonymousUser

from app import routes

app.run(debug=True)
