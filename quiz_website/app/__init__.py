"""init"""

from flask import Flask
from flask_login import LoginManager
from prisma import register
from app import environments
from app.db import db


register(db)
app = Flask(__name__)
# login_manager = LoginManager()

app.config['SECRET_KEY'] = environments.SECRET_KEY

# login_manager.init_app(app)

from app import routes


app.run(debug=True)
