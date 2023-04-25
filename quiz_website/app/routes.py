from flask import render_template, url_for, flash, request
from prisma import Prisma

from app import forms, db, app


# Renders home page
@app.get('/')
def home():
    return render_template('home.html')


# Account page, no session shows signup/login
@app.route('/account', methods=['GET', 'POST'])
def account():
    form = forms.SignUp()
    if form.validate_on_submit():
        print('success')
    return render_template('account.html', form=form)


