from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from prisma.models import User

from app import forms, login_manager, app
from app.user import UserClass


# Check if the user object is still valid
@login_manager.user_loader
def user_loader(user_id):
    user = User.prisma().find_first(
        where={
            'user_id' : int(user_id)
        }
    )
    return UserClass(user.__dict__)


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
        User.prisma().create(
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
    if 'login-form' in request.form and login_form.validate_on_submit():
        username = login_form.login_username.data
        password = login_form.login_password.data
        remember = login_form.remember.data
        user_data = User.prisma().find_first(
            where={
                'username' : username
            }
        )
        print(user_data)
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


# page to create new quiz
@app.get('/quiz/create')
def quiz_creation():
    quiz_form = forms.Quiz()
    return render_template('create_quiz.html', quiz_form=quiz_form)


@app.post('/quiz/create_quiz')
def create_quiz():
    quiz_form = forms.Quiz()
    print(request.form)
    if 'quiz-form' in request.form and quiz_form.validate_on_submit():
        print(request.form)
    return redirect(url_for('home'))