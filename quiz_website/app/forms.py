from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, RadioField
from wtforms.validators import DataRequired


# Accounts
class SignUp(FlaskForm):
    signup_username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder' : 'Username'})
    signup_email = EmailField('Email', validators=[DataRequired()], render_kw={'placeholder' : 'Email'})
    signup_password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder' : 'Password'})
    signup_password_confirm = PasswordField('ConfirmPassword', validators=[DataRequired()], render_kw={'placeholder' : 'Confirm password'})
    submit = SubmitField('Signup', name='signup-form', id='signup-form')


class Login(FlaskForm):
    login_username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder' : 'Username'})
    login_password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder' : 'Password'})
    remember = BooleanField('Remember me')
    submit = SubmitField('Login', name='login-form', id='login-form')


# Quizzes
class QuizInfo(FlaskForm):
    name = StringField('Quiz name', validators=[DataRequired()], render_kw={'placeholder' : 'Quiz name'})
    desc = StringField('Quiz description', validators=[DataRequired()], render_kw={'placeholder' : 'Quiz description'})
    submit = SubmitField('Create', name='quiz-info', id='quiz-info')


class WrittenQuestion(FlaskForm):
    written_question = StringField('Question', validators=[DataRequired()], render_kw={'placeholder' : 'Question'})
    written_answer = StringField('Answer', validators=[DataRequired()], render_kw={'placeholder' : 'Answer'})
    submit = SubmitField('Create', name='quiz-written', id='quiz-written')


class TrueFalseQuestion(FlaskForm):
    fact_statement = StringField('Statement', validators=[DataRequired()], render_kw={'placeholder' : 'Statement'})
    fact_answer = RadioField('Answer', choices=[('true', 'True'), ('false', 'False')] , validators=[DataRequired()])
    submit = SubmitField('Create', name='quiz-fact', id='quiz-fact')


class MultipleChoiceQuestion(FlaskForm):
    multi_question = StringField('Question', validators=[DataRequired()], render_kw={'placeholder' : 'Question'})
    correct_answer = StringField('Answer', validators=[DataRequired()], render_kw={'placeholder' : 'Answer'})
    false_one = StringField('False answer', validators=[DataRequired()], render_kw={'placeholder' : 'False answer'})
    false_two = StringField('False answer', validators=[DataRequired()], render_kw={'placeholder' : 'False answer'})
    false_three = StringField('False answer', validators=[DataRequired()], render_kw={'placeholder' : 'False answer'})
    submit = SubmitField('Create', name='quiz-multi', id='quiz-multi')
