from itsdangerous import URLSafeTimedSerializer
from secrets import token_urlsafe

from app import app


def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dump(email, salt=app.config['TOKEN_SALT'])


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