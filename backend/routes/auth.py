from flask import (
    Blueprint,
    session,
    request,
    jsonify
)
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError
from models import db, User
from helpers.tokens import create_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

CURR_USER_KEY = "curr_user"

def do_login(user):
    session[CURR_USER_KEY] = user.id
    session.permanent = True

user_auth_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["username", "password"]
}

@auth_bp.route("/token", methods=["POST"])
def token():
    try:
        validate(instance=request.json, schema=user_auth_schema)
    except ValidationError as e:
        return jsonify({"error": e.message}), 400

    try:
        username = request.json.get('username')
        password = request.json.get('password')
        user = User.authenticate(username, password)
        
        if not user:
            return jsonify({"error": "Invalid username or password"}), 401
        
        token = create_token(user)
        do_login(user)
        return jsonify({"token": token,"user": {"id": user.id, "username": user.username}}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500


@auth_bp.route("/signup", methods=["POST"])
def signup():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        user = User.signup(
            username=username,
            password=password,
            email=email
        )
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "Username or email already taken"}), 400

    token = create_token(user)
    do_login(user)
    return jsonify({"message": "User created successfully", "token": token, "user": {"id": user.id, "username": user.username}}), 201