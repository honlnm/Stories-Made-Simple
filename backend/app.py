import os
from flask import (
    Flask,
    session,
    g,
    jsonify,
    request
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from models import db, connect_db, User
from routes.auth import auth_bp
from routes.user import user_bp


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "postgresql:///stories",
)
app.config["SCHEDULER_API_ENABLED"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config["SECRET_KEY"] = os.getenv("secret_key")

toolbar = DebugToolbarExtension(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)

connect_db(app)
with app.app_context():
    db.create_all()
    db.session.commit()

CURR_USER_KEY = "curr_user"

############## GLOBAL USER ##############

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None