from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy(session_options={"expire_on_commit": False})

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    plot_series = db.relationship("PlotSeries", backref="users")

    @classmethod
    def signup(cls, username, email, password):
        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")
        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False
    
class PlottingFramework(db.Model):
    __tablename__ = "plotting_frameworks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    num_plot_points = db.Column(db.Integer, nullable=False)
    img_rep = db.Column(db.Text, nullable=False)
    plotting_points = db.relationship("PlottingPoint")
    plot_series = db.relationship("PlotSeries")

class SeriesType(db.Model):
    __tablename__ = "series_types"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    num_of_books = db.Column(db.Integer, nullable=False)
    plot_series = db.relationship("PlotSeries")

class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    avg_word_count = db.Column(db.Integer, nullable=False)
    min_word_count = db.Column(db.Integer, nullable=False)
    max_word_count = db.Column(db.Integer, nullable=False)
    plot_series = db.relationship("PlotSeries")

class  PlottingPoint(db.Model):
    __tablename__ = "plotting_points"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plot_step = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable = False)
    percent_of_story = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    framework_id = db.Column(db.Integer, db.ForeignKey("plotting_frameworks.id", ondelete="cascade"))
    plot_points = db.relationship("PlotPoints")

class PlotSeries(db.Model):
    __tablename__ = "plot_series"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_of_books = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False)
    plot = db.relationship("Plot", backref="plot_sereies")
    framework_id = db.Column(db.Integer, db.ForeignKey("plotting_frameworks.id", ondelete="cascade"))
    series_type_id = db.Column(db.Integer, db.ForeignKey("series_types.id", ondelete="cascade"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id", ondelete="cascade"))

class Plot(db.Model):
    __tablename__ = "plot"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_title = db.Column(db.Text, nullable=False)
    total_word_count = db.Column(db.Integer, nullable=False)
    words_per_chapter = db.Column(db.Integer, nullable=False)
    plot_series_id = db.Column(db.Integer, db.ForeignKey("plot_series.id", ondelete="cascade"))
    plot_points = db.relationship("PlotPoints", backref="plot")

class PlotPoints(db.Model):
    __tablename__ = "plot_points"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plot_point_id = db.Column(db.Integer, db.ForeignKey("plotting_points.id", ondelete="cascade"))
    plot_id = db.Column(db.Integer, db.ForeignKey("plot.id", ondelete="cascade"))

############## CONNECT DB ##############

def connect_db(app):
    db.app = app
    db.init_app(app)