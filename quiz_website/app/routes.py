import datetime
from flask import render_template, url_for, flash, redirect, request, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from prisma import models

from app import forms, login_manager, app
from app.user import UserClass


QUESTION_TYPES = {
        0: 'True/False',
        1: 'Written',
        2: 'Multiple choice'
    }


def get_one_quiz(quiz_id):
    quiz = models.Quiz.prisma().find_first(
        include={
            'questions': {
                'include': {
                    'answers': True
                }
            }
        },
        where={
            'quiz_id': quiz_id
        }
    )
    return quiz


# Get the id of the newley created question
def get_question_id():
    question_id = models.Question.prisma().find_first(
        order={
            'question_id': 'desc'
        }
    ).question_id
    return question_id


# Check if the user object is still valid
@login_manager.user_loader
def user_loader(user_id):
    user = models.User.prisma().find_first(
        where={
            'user_id': int(user_id)
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
            data={
                'username': username,
                'email': email,
                'password_hash': password_hash,
            }
        )
    return redirect(url_for('account'))


# Login user if creds are valid
@app.post('/account/login')
def account_login():
    login_form = forms.Login()
    if 'login-form' in request.form and login_form.validate_on_submit():
        username = login_form.login_username.data
        password = login_form.login_password.data
        remember = login_form.remember.data
        user_data = models.User.prisma().find_first(
            where={
                'username': username
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
            'questions': {
                'include': {
                    'answers': True
                }
            }
        }
    )
    return render_template('display_quiz.html', quiz=quiz, types=QUESTION_TYPES)


# View individual quizzes
# User edits their own quizzes here
@app.get('/quiz/view/<int:quiz_id>')
def view_one_quiz(quiz_id):
    written_form = forms.WrittenQuestion()
    fact_form = forms.TrueFalseQuestion()
    multi_choice_form = forms.MultipleChoiceQuestion()
    quiz = get_one_quiz(quiz_id)
    session['current_quiz_id'] = quiz_id
    return render_template('display_one_quiz.html',
                           quiz=quiz,
                           types=QUESTION_TYPES,
                           written_form=written_form,
                           fact_form=fact_form,
                           multi_choice_form=multi_choice_form,
                           )


# View and create new quizzes here
@app.get('/quiz/view/my_quizzes')
@login_required
def quiz_creation():
    user_quizzes = models.Quiz.prisma().find_many(
        where={
            'user_id': int(current_user.user_id)
        }
    )
    quiz_info = forms.QuizInfo()
    return render_template('user_quiz.html', quiz_info=quiz_info, user_quizzes=user_quizzes)


# Create new quiz and questions for that quiz
@app.post('/quiz/create/<form_type>')
@login_required
def create(form_type):
    # Create new quiz
    if form_type == '0':
        form = forms.QuizInfo()
        if 'quiz-info' in request.form and form.validate_on_submit():
            models.Quiz.prisma().create(
                data={
                    'name': form.name.data,
                    'description': form.desc.data,
                    'user_id': int(current_user.user_id)
                }
            )
            new_quiz_id = models.Quiz.prisma().find_first(
                order={
                    'quiz_id': 'desc',
                }
            ).quiz_id
            return redirect(url_for('view_one_quiz', quiz_id=new_quiz_id))
    
    # Check if the current user id is same as author of quiz
    quiz_id = session.get('current_quiz_id', None)
    quiz_user = models.Quiz.prisma().find_first(
        where={
            'quiz_id': quiz_id
        }
    ).user_id
    if quiz_user != int(current_user.user_id):
        return redirect(url_for('view_one_quiz', quiz_id=quiz_id))
    
    # Create new question for specific quiz
    # Create written answer, add question and answer to database
    elif form_type == '1':
        form = forms.WrittenQuestion()
        if 'quiz-written' in request.form and form.validate_on_submit():
            models.Question.prisma().create(
                data={
                    'quiz_id': quiz_id,
                    'question': form.written_question.data,
                    'type': int(form_type)
                }
            )
            question_id = get_question_id()
            models.Answer.prisma().create(
                data={
                    'question_id': question_id,
                    'answer': form.written_answer.data
                }
            )

    # Create true and false questions for the quiz
    elif form_type == '2':
        form = forms.TrueFalseQuestion()
        if 'quiz-fact' in request.form and form.validate_on_submit():
            # create true statement as question in database
            models.Question.prisma().create(
                data={
                    'quiz_id': quiz_id,
                    'question': form.true_statement.data,
                    'type': int(form_type)
                }
            )
            question_id = get_question_id()
            models.Answer.prisma().create(
                data={
                    'question_id': question_id,
                    'answer': 'True'
                }
            )
            # create false statement as question in database
            models.Question.prisma().create(
                data={
                    'quiz_id': quiz_id,
                    'question': form.false_statement.data,
                    'type': int(form_type)
                }
            )
            question_id = get_question_id()
            models.Answer.prisma().create(
                data={
                    'question_id': question_id,
                    'answer': 'False'
                }
            )

    # Create multiple choice questions for quiz
    elif form_type == '3':
        form = forms.MultipleChoiceQuestion()
        if 'quiz-multi' in request.form and form.validate_on_submit():
            # Create question and correct answer
            models.Question.prisma().create(
                data={
                    'quiz_id': quiz_id,
                    'question': form.multi_question.data,
                    'type': int(form_type)
                }
            )
            question_id = get_question_id()
            models.Answer.prisma().create(
                data={
                    'question_id': question_id,
                    'answer': form.correct_answer.data
                }
            )
            # Create false answers in the database
            for answer in [form.false_one.data, form.false_two.data, form.false_three.data]:
                models.FalseAnswer.prisma().create(
                    data={
                        'question_id': question_id,
                        'answer': answer,
                    }
                )
    return redirect(url_for('view_one_quiz', quiz_id=quiz_id))
  

# Attempting a quiz
@app.get('/quiz/attempt/<int:quiz_id>')
@login_required
def attempt_quiz(quiz_id):
    session['start_time'] = datetime.datetime.now()
    quiz = get_one_quiz(quiz_id)
    # Get all answers for multi choice questions
    answers = models.Answer.prisma().find_many(
        where={
            'quiz_id': quiz_id,
        }
    )
    return render_template('attempt_quiz.html', quiz=quiz, answers=answers)


# Submit quiz attempt
