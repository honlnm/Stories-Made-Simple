import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def create_token(user):

    if 'isAdmin' not in user:
        raise ValueError("create_token passed user without isAdmin property")

    payload = {
        'username': user['username'],
        'isAdmin': user.get('isAdmin', False),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

