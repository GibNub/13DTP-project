from flask import render_template
from prisma import Prisma

import forms
from app import app

db = Prisma()

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')