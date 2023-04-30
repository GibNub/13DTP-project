from flask import render_template, url_for, flash, redirect, request
from prisma import Prisma
from prisma.models import User
from werkzeug.security import generate_password_hash, check_password_hash

from app import forms, app


# Renders home page
@app.get('/')
def home():
    return render_template('home.html')


# Account page, no session shows signup/login
@app.get('/account')
def account():
    signup_form = forms.SignUp()
    login_form = forms.Login()
    return render_template('account.html', signup_form=signup_form, login_form=login_form)


@app.post('/account/signup')
def account_signup():
    signup_form = forms.SignUp()
    if request.form:
        print('Information received')
    # Create user account
    if 'signup-form' in request.form and signup_form.validate_on_submit():
        username = signup_form.signup_username.data
        email = signup_form.signup_email.data
        password_hash = generate_password_hash(signup_form.signup_password.data, salt_length=16)
        User.prisma().create(
            data = {
                'username'  : username,
                'email'     : email,
                'password_hash'  : password_hash,
                'admin'     : 0,
                'confirmed' : 0,
            }   
        )
        print('Account created')
    return redirect(url_for('account'))

@app.post('/account/login')
def account_login():
    login_form = forms.Login()
    if 'login-form' in request.form and login_form.validate_on_submit():
        username = login_form.login_username.data
        password = login_form.login_password.data
        user_data = User.prisma().find_first(
            where={
                'username' : username
            }
        )
        # Check usernames and passwords
        if check_password_hash(user_data.password_hash, password):
            print('logged')
        else:
            print('user or pass incorrect')
    return redirect(url_for('account'))
