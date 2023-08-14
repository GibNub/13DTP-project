import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
TOKEN_SALT = os.getenv('TOKEN_SALT')
