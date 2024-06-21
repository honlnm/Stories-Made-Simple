from flask import (
    Blueprint,
    session,
    request,
    jsonify,
    g
)
from sqlalchemy.exc import IntegrityError
from models import db, User

user_bp = Blueprint("user", __name__, url_prefix="/user")

def do_logout(user_id):
    if user_id in session:
        del session[user_id]

@user_bp.route("/<int:user_id>")
def show_user(user_id):
    if user_id != g.user.id:
        return jsonify({"error": "Unauthorized"}), 401
    user = User.query.get_or_404(user_id)
    return jsonify({"user": {"id": user.id, "username": user.username, "email": user.email}}), 201

@user_bp.route("/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    if user_id != g.user.id:
        return jsonify({"error": "Unauthorized"}), 401
    user = User.query.get_or_404(user_id)

    data = request.json

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if User.authenticate(username=username, password=password):
        user.username = username
        user.email = email
        db.session.commit()
        return jsonify({"message": f"{user.username} updated successfully", "user": {"id": user.id, "username": user.username, "email": user.email}}), 201
    
@user_bp.route("/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    if user_id != g.user.id:
        return jsonify({"error": "Unauthorized"}), 401
    user = User.query.get_or_404(user_id)

    data = request.json

    username = data.get('username')
    password = data.get('password')

    if User.authenticate(username=username, password=password):
        do_logout(user.id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 201
    