"""init"""

from flask import Flask
from flask_login import LoginManager
from app import envrionments

app = Flask(__name__)
# login_manager = LoginManager()

app.config['SECRET_KEY'] = envrionments.SECRET_KEY

# login_manager.init_app(app)

from app import routes


app.run(debug=True)
