from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class SignUp(FlaskForm):
    signup_username = StringField('Username', validators=[DataRequired()])
    signup_email = StringField('Email', validators=[DataRequired()])
    signup_password = PasswordField('Password', validators=[DataRequired()])


class Login(FlaskForm):
    login_username = StringField('Username', validators=[DataRequired()])
    login_password = PasswordField('Password', validators=[DataRequired()])