from flask import (
    Blueprint,
    session,
    request,
    jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

CURR_USER_KEY = "curr_user"

def do_login(user):
    session[CURR_USER_KEY] = user.id
    session.permanent = True

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

    access_token = create_access_token(identity=user.id)
    return jsonify({"message": "User created successfully", "access_token": access_token, "user": {"id": user.id, "username": user.username}}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token, "user": {"id": user.id, "username": user.username}}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401