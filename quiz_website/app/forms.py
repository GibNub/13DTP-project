from flask_wtf import FlaskForm
import wtforms
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class SignUp(FlaskForm):
    signup_username = StringField('Username', validators=[DataRequired()])
    signup_email = EmailField('Email', validators=[DataRequired()])
    signup_password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Signup', name='signup-form', id='signup-forn')


class Login(FlaskForm):
    login_username = StringField('Username', validators=[DataRequired()])
    login_password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login', name='login-form', id='login-form')