from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from prisma import models

from app import forms, login_manager, app
from app.user import UserClass


# Check if the user object is still valid
@login_manager.user_loader
def user_loader(user_id):
    user = models.User.prisma().find_first(
        where={
            'user_id' : int(user_id)
        }
    )
    if user:
        return UserClass(user.__dict__)
    else:
        return None


# Renders home page
@app.get('/')
def home():
    return render_template('home.html')


# User Account views
# Account page, no session shows signup/login
@app.get('/account')
def account():
    signup_form = forms.SignUp()
    login_form = forms.Login()
    return render_template('account_manage.html', signup_form=signup_form, login_form=login_form)


# Log user out
@app.get('/account/logout')
@login_required
def account_logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('account'))


# Sign up request
@app.post('/account/signup')
def account_signup():
    signup_form = forms.SignUp()
    # Create user account
    if 'signup-form' in request.form and signup_form.validate_on_submit():
        username = signup_form.signup_username.data
        email = signup_form.signup_email.data
        # Hash password and store user data
        password_hash = generate_password_hash(signup_form.signup_password.data, salt_length=16)
        models.User.prisma().create(
            data = {
                'username'       : username,
                'email'          : email,
                'password_hash'  : password_hash,
            }   
        )
    return redirect(url_for('account'))


# Logs user in if creds are valid
@app.post('/account/login')
def account_login():
    login_form = forms.Login()
    print(request.form)
    if 'login-form' in request.form and login_form.validate_on_submit():
        username = login_form.login_username.data
        password = login_form.login_password.data
        remember = login_form.remember.data
        user_data = models.User.prisma().find_first(
            where={
                'username' : username
            }
        )
        if not user_data:
            flash('User does not exist')
        else:
            user = UserClass(user_data.__dict__)
            # Check usernames and passwords
            if check_password_hash(user.password, password):
                login_user(user, remember=remember)
            else:
                flash('Username or password is incorrect')
    return redirect(url_for('account'))


# Settings page
@app.get('/account/settings')
@login_required
def settings():
    return render_template('settings.html')


# Display all the quizzes in a page
@app.get('/quiz/view/all')
def view_quiz():
# Get quiz info, the questions, and the answer to each question
    quiz = models.Quiz.prisma().find_many(
        include={
            'questions' : {
                'include' : {
                    'answers' : True
                }
            }
        }
    )
    return render_template('display_quiz.html', quiz=quiz)


# Pages to create quizzes
# page to create new quiz
@app.get('/quiz/create')
@login_required
def quiz_creation():
    quiz_form = forms.Quiz()
    return render_template('create_quiz.html', quiz_form=quiz_form)


@app.post('/quiz/create_quiz')
@login_required
def create_quiz():
    quiz_form = forms.Quiz()
    if 'quiz-form' in request.form and quiz_form.validate_on_submit():
        questions = request.form.getlist('question')
        answers = request.form.getlist('answer')
        question_type = request.form.getlist('question-type')
        # Check if lengths of each form field are equal by comparing each list to the questions list
        info = [questions, answers, question_type]
        if not all([len(x) == len(info[0]) for x in info]):
            flash('The quiz you created was invalid as the amount of questions and answers are not equal')
            return redirect(url_for('quiz_creation'))
        # Create quiz with name and desc
        models.Quiz.prisma().create(
            data={
                'name' : quiz_form.name.data,
                'description' : quiz_form.desc.data,
                'user_id' : int(current_user.user_id)
            }
        )
        # Create questions and answers
        quiz_id = models.Quiz.prisma().find_first(
            order={
                'quiz_id' : 'desc'
            }
        ).quiz_id
        models.Question.prisma().create(
            data={
                'quiz_id' : quiz_id,
                'question' : questions[0],
                'type' : 1,
            }
        )
        # Create answer 
        question_id = models.Question.prisma().find_first(
            order={
                'question_id' : 'desc'
            }
        ).question_id
        models.Answer.prisma().create(
            data={
                'question_id' : question_id,
                'answer' : answers[0]
            }
        )
    return redirect(url_for('home'))
