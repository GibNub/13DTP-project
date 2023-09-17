from time import time
from math import floor
from flask import render_template, url_for, flash, redirect, abort, request, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from profanity_check import predict_prob
from prisma import models

from app import forms, login_manager, app
from app.user import UserClass
from app.email import send_email
from app.token_id import generate_token, confirm_token


QUESTION_TYPES = {
        1: 'Fact',
        2: 'Written',
        3: 'Multiple choice'
    }


MAX_SCORE = 1000
# Lower value means will catch more words (0 to 1)
FILTER_LENIANCY = 0.8
def is_profane(text):
    return predict_prob([text]) > FILTER_LENIANCY

# Quick function to get one quiz and all related information
def get_one_quiz(quiz_id):
    quiz = models.Quiz.prisma().find_first(
        # Get all questions, answers, and false answers if it exists from question table for the given quiz
        include={
            'questions': {
                'include': {
                    'answers': True,
                    'falseAnswer': True,
                }
            },
            # Get all submitted scores with user info from score table
            'user_score':  {
                'include': {
                    'user': True,
                }
            },
            'user': True,
        },
        where={
            'quiz_id': quiz_id
        }
    )
    return quiz


# Get the id of the newley created question
def get_question_id():
    '''
    Quickly get the id of newly created question,
    easier to link answer
    '''
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
    return render_template('home.html', page_header='Home')


# Account page, no session shows signup/login forms instead
@app.get('/account')
def account():
    signup_form = forms.SignUp()
    login_form = forms.Login()
    return render_template('account_manage.html', signup_form=signup_form, login_form=login_form, page_header='Manage account')


# Logout user
@app.get('/account/logout')
@login_required
def account_logout():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('account'))


# Sign up request
@app.post('/account/signup')
def account_signup():
    signup_form = forms.SignUp()
    error = False
    # Create user account
    if 'signup-form' in request.form and signup_form.validate_on_submit():
        username = signup_form.signup_username.data
        email = signup_form.signup_email.data
        password = signup_form.signup_password.data
        confirm_pass = signup_form.signup_password_confirm.data
        # Check if username or email already exists
        existsing_info = models.User.prisma().find_many()
        # Get each existing info into lists
        existing_usernames = [x.username for x in existsing_info]
        existing_emails = [x.email for x in existsing_info]
        if username in existing_usernames or email in existing_emails:
            flash('Username or email already exists', category='error')
            error = True
        # Check for profanity in username
        if is_profane(username):
            flash('Username contains profanity', category='error')
            error = True
        # Check for min and max length
        if len(username) > 32 or len(username) < 3:
            flash('Username is too short or too long', category='error')
            error = True
        if len(password) < 3:
            flash('Password is too short', category='error')
            error = True
        # Check if passwords match
        if password != confirm_pass:
            flash('Password do not match', category='error')
            error = True
        if error:
            return redirect(url_for('account'))
        # Hash password and store user data
        password_hash = generate_password_hash(signup_form.signup_password.data, salt_length=16)
        models.User.prisma().create(
            data={
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'confirmed': False,
            }
        )
        flash('Account created, please log in', category='info')
    # TODO setup email
    # token = generate_token(email)
    # confirm_url = url_for('confirm_email', token=token, _external=True)
    # template = render_template('email.html', confirm=confirm_url)
    # send_email(email, subject='Confirm email', template=template)
    return redirect(url_for('account'))


# Pre-confirmation page
@app.get('/account/unconfirmed')
def unconfirmed():
    return render_template('confirm.html')


# Confirm user with token
@app.get('/account/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
        print('e')
    except:
        flash('token invalid', category='error')
    if not email:
        return redirect(url_for('account'))
    user_data = models.User.prisma().find_first(
        where={
            'email': email,
        }
    )
    user = UserClass(user_data.__dict__)
    if user.confirmed:
        flash('already confirmed', category='error')
        return redirect(url_for('account'))
    # Confirm user in database
    else:
        models.User.prisma().update(
            where={
                'username': session.get('username')
            },
            data={
                'confirmed': True
            }
        )
    return redirect(url_for('home'))


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
            flash('Login failed. Username or password is incorrect', category='error')
            return redirect(url_for('account'))
        user = UserClass(user_data.__dict__)
        # Check usernames and passwords
        if check_password_hash(user.password, password):
            if user.confirmed:
                session['username'] = None
                login_user(user, remember=remember)
                flash('Logged in', category='info')
            else:
                # Will update when email confirmatin implemented
                session['username'] = None
                login_user(user, remember=remember)
                # session['username'] = user.username
                # return redirect(url_for('unconfirmed'))
        else:
            flash('Login failed. Username or password is incorrect', category='error')
            return redirect(url_for('account'))
    return redirect(url_for('home'))


# Settings page
@app.get('/account/settings')
@login_required
def settings():
    return render_template('settings.html')


# Display all the quizzes in a page
@app.get('/quiz/view/all')
def view_quiz():
    query = session.get('search_query', None)
    # Use result from search query for database query, otherwise get all quizzes
    if not query:
        # Get all quizzes from quiz table, include 3 questions and answers to each
        quiz = models.Quiz.prisma().find_many(
            include={
                'questions': {
                    'take': 3,
                    'include': {
                        'answers': True
                    }
                }
            }
        )
    else:
        # Get all quizzes from quiz table, include 3 questions and answers to each
        # Where the the title contains the search query
        quiz = models.Quiz.prisma().find_many(
            include={
                'questions': {
                    'take': 3,
                    'include': {
                        'answers': True
                    }
                }
            },
            where={
                'name': {
                    'contains': query
                }
            }
        )
        session.pop('search_query')
    return render_template('display_quiz.html', quiz=quiz, types=QUESTION_TYPES, page_header='Browse quizzes')


# Search for quizzes
@app.post('/quiz/view/query')
def view_query_quiz():
    # Get quizzes where the user query is in the name of a quiz
    query = request.form.get('query')
    session['search_query'] = query
    return redirect(url_for('view_quiz'))

# View individual quizzes
# User edits their own quizzes on this page
@app.get('/quiz/view/<int:quiz_id>')
def view_one_quiz(quiz_id):
    written_form = forms.WrittenQuestion()
    fact_form = forms.TrueFalseQuestion()
    multi_choice_form = forms.MultipleChoiceQuestion()
    quiz = get_one_quiz(quiz_id)
    if not quiz:
        abort(404)
    # Get all submitted scores for a quiz
    scores = models.Score.prisma().find_many(
        where={
            'quiz_id': quiz_id,
        },
        include={
            'user': True
        }
    )

    # Store scores and times on list, then sort in order of score then time
    scores = [(s.score, s.time, s.user.username) for s in scores]
    scores.sort()
    session['current_quiz_id'] = quiz_id
    return render_template('display_one_quiz.html',
                            quiz=quiz,
                            types=QUESTION_TYPES,
                            written_form=written_form,
                            fact_form=fact_form,
                            multi_choice_form=multi_choice_form,
                            quiz_id=quiz_id,
                            page_header='View quiz'
                            )


# View and create new quizzes
@app.get('/quiz/view/my_quizzes')
@login_required
def quiz_creation():
    # Get all quizzes and their questions made by a specific user
    user_quizzes = models.Quiz.prisma().find_many(
        where={
            'user_id': int(current_user.user_id)
        },
        include={
            'questions': True
        }
    )
    quiz_info = forms.QuizInfo()
    return render_template('user_quiz.html', quiz_info=quiz_info, user_quizzes=user_quizzes, types=QUESTION_TYPES, page_header='My quizzes')


# Create new quiz and questions for that quiz
@app.post('/quiz/create/<form_type>')
@login_required
def create(form_type):
    # Create new quiz
    def complete(ref_quiz_id):
        return redirect(url_for('view_one_quiz', quiz_id=ref_quiz_id))
    if form_type == '0':
        form = forms.QuizInfo()
        if 'quiz-info' in request.form and form.validate_on_submit():
            if is_profane(form.name.data):
                flash('Quiz name contains profanity', category='error')
                return redirect(url_for('quiz_creation'))
            models.Quiz.prisma().create(
                data={
                    'name': form.name.data,
                    'description': form.desc.data,
                    'user_id': int(current_user.user_id)
                }
            )
            # Get created quiz id to redirect user
            new_quiz_id = models.Quiz.prisma().find_first(
                order={
                    'quiz_id': 'desc',
                }
            ).quiz_id
            flash('Quiz created', category='info')
            complete(new_quiz_id)

    # Editing quiz
    
    # Check if the current user id is same as user id of quiz creators
    quiz_id = session.get('current_quiz_id', None)
    quiz_user = models.Quiz.prisma().find_first(
        where={
            'quiz_id': quiz_id
        }
    ).user_id
    if quiz_user != int(current_user.user_id):
        complete(quiz_id)

    # Create new question for specific quiz
    # Get question_id function used to link answer to created question

    # Create true and false questions for the quiz
    elif form_type == '1':
        form = forms.TrueFalseQuestion()
        if 'quiz-fact' in request.form and form.validate_on_submit():
            if is_profane(form.fact_statement.data):
                flash('Question contains profanity', category='error')
                complete(quiz_id)
            # Create true statement as question in database
            models.Question.prisma().create(
                data={
                    'quiz_id': quiz_id,
                    'question': form.fact_statement.data,
                    'type': int(form_type)
                }
            )
            # Create answer for fact question
            question_id = get_question_id()
            models.Answer.prisma().create(
                data={
                    'question_id': question_id,
                    'answer': form.fact_answer.data
                }
            )
            flash('Fact question created', category='info')

    # Create written question
    elif form_type == '2':
        form = forms.WrittenQuestion()
        if 'quiz-written' in request.form and form.validate_on_submit():
            if is_profane(form.written_question.data) or is_profane(form.written_answer.data):
                flash('Question contains profanity', category='error')
                complete(quiz_id)
            models.Question.prisma().create(
                data={
                    'quiz_id': quiz_id,
                    'question': form.written_question.data,
                    'type': int(form_type)
                }
            )
            # Add answer for written question
            question_id = get_question_id()
            models.Answer.prisma().create(
                data={
                    'question_id': question_id,
                    'answer': form.written_answer.data
                }
            )
            flash('Written question created', category='info')

    # Create multiple choice questions for quiz
    elif form_type == '3':
        form = forms.MultipleChoiceQuestion()
        if 'quiz-multi' in request.form and form.validate_on_submit():
            if is_profane(form.multi_question.data) or is_profane(form.correct_answer.data):
                flash('Question contains profanity', category='error')
                complete(quiz_id)
            # Create question
            models.Question.prisma().create(
                data={
                    'quiz_id': quiz_id,
                    'question': form.multi_question.data,
                    'type': int(form_type)
                }
            )
            # Create answer
            question_id = get_question_id()
            models.Answer.prisma().create(
                data={
                    'question_id': question_id,
                    'answer': form.correct_answer.data
                }
            )
            # Create false answers in the database if question is multichoice
            for answer in [form.false_one.data, form.false_two.data, form.false_three.data]:
                if is_profane(answer):
                    flash('Question contains profanity', category='error')
                    complete(quiz_id)
                models.FalseAnswer.prisma().create(
                    data={
                        'question_id': question_id,
                        'answer': answer,
                    }
                )
            flash('Multiple choice question created', category='info')
    return redirect(url_for('view_one_quiz', quiz_id=quiz_id))


# Start quiz attempt
@app.get('/quiz/attempt/<int:quiz_id>')
@login_required
def attempt_quiz(quiz_id):
    session['start_time'] = time()
    quiz = get_one_quiz(quiz_id)
    # Get all the question ids from the current quiz
    question_ids = []
    for q in quiz.questions:
        question_ids.append(q.question_id)
    # Get all incorrect answers for any multi choice questions
    false_answers = models.FalseAnswer.prisma().find_many(
        where={
            'question_id': {'in': question_ids},
        }
    )
    
    return render_template('attempt_quiz.html',
                           quiz=quiz,
                           false_answers=false_answers,
                           page_header='Attempting quiz'
                           )


# Submit quiz attempt and store score
@app.post('/quiz/attempt/<int:quiz_id>/submit')
@login_required
def submit_quiz(quiz_id):
    if not current_user.user_id:
        return redirect(url_for('home'))
    time_now = time()
    user_answers = request.form
    quiz = get_one_quiz(quiz_id)
    # Define points per question (ppq)
    ppq = MAX_SCORE / len(quiz.questions)
    # Validate submitted attempt
    if len(quiz.questions) != len(user_answers):
        flash('The submitted attempt is not valid', 'error')
        return redirect(url_for('view_one_quiz', quiz_id=quiz_id))
    # Check if each answer is correct or incorrect, then increment amount correct by one
    correct_count = 0
    for question in quiz.questions:
        if user_answers[str(question.question_id)] == question.answers[0].answer:
            correct_count += 1

    # Calculate final score and time
    delta_time = time_now - session.get('start_time')
    final_score = floor(correct_count * ppq)
    # Submit score in database
    models.Score.prisma().create(
        data={
            'quiz_id': quiz.quiz_id,
            'user_id': int(current_user.user_id),
            'score': final_score,
            'time': int(delta_time)
        }
    )
    flash('Attempt submitted', category='info')
    return redirect(url_for('view_one_quiz', quiz_id=quiz_id))


# User pages
@app.get('/user/<int:user_id>')
def user_page(user_id):
    user = models.User.prisma().find_first(
        # Get user and all their created quizzes
        where={
            'user_id': user_id
        },
        include={
            'quizzes': True,
            'quiz_score': True
        }
    )
    return render_template('user.html', user=user, page_header='User page')


# 404 error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500
