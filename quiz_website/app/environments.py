import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', default='super_secret_key')
TOKEN_SALT = os.getenv('TOKEN_SALT', default='super_secret_salt')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', default='super_secret_password')
