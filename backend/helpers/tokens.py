import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def create_token(user):

    payload = {
        'username': user.username
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

