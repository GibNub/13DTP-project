from flask_wtf import FlaskForm
import wtforms
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


# Accounts
class SignUp(FlaskForm):
    signup_username = StringField('Username', validators=[DataRequired()])
    signup_email = EmailField('Email', validators=[DataRequired()])
    signup_password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Signup', name='signup-form', id='signup-form')


class Login(FlaskForm):
    login_username = StringField('Username', validators=[DataRequired()])
    login_password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login', name='login-form', id='login-form')


class Quiz(FlaskForm):
    name = StringField(validators=[DataRequired()])
    desc = StringField(validators=[DataRequired()])
    # Quiz question info
    submit = SubmitField('Create', name='quiz-form', id='quiz-form')
