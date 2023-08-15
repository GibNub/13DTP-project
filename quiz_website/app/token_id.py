from itsdangerous import URLSafeTimedSerializer

from app import app


def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['TOKEN_SALT'])


def confirm_token(token, expiration=600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
           token,
           salt=app.config['TOKEN_SALT'],
           max_age=expiration
        )
    except:
        return False
    return email