from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy(session_options={"expire_on_commit": False})

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    plot = db.relationship("Plot", backref="users")

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
    plot = db.relationship("Plot")

class SeriesType(db.Model):
    __tablename__ = "series_types"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    num_of_books = db.Column(db.Integer, nullable=False)
    plot = db.relationship("Plot")

class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    avg_word_count = db.Column(db.Integer, nullable=False)
    min_word_count = db.Column(db.Integer, nullable=False)
    max_word_count = db.Column(db.Integer, nullable=False)
    plot = db.relationship("Plot")

class  PlottingPoint(db.Model):
    __tablename__ = "plotting_points"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plot_step = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable = False)
    percent_of_story = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    framework_id = db.Column(db.Integer, db.ForeignKey("plotting_frameworks.id", ondelete="cascade"))
    plot_points = db.relationship("PlotPoints")

class Plot(db.Model):
    __tablename__ = "plot"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_of_books = db.Column(db.Integer, nullable=False)
    book_num = db.Column(db.Integer, nullable=False, default=1)
    book_title = db.Column(db.Text, nullable=False)
    series_title=db.Column(db.Text, nullable=False, default="Not Applicable")
    book_word_count=db.Column(db.Integer, nullable=False)
    avg_words_per_chapter=db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    framework_id = db.Column(db.Integer, db.ForeignKey("plotting_frameworks.id", ondelete="cascade"))
    series_type_id = db.Column(db.Integer, db.ForeignKey("series_types.id", ondelete="cascade"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id", ondelete="cascade"))
    plot_points = db.relationship("PlotPoints", backref="plot")

    @classmethod
    def create(cls,
               user_id,
               num_of_books,
               book_num,
               book_title,
               series_title,
               book_word_count,
               avg_words_per_chapter,
               last_updated,
               framework_id,
               series_type_id,
               genre_id
    ):
        plot = Plot(
            user_id=user_id,
            num_of_books=num_of_books,
            book_num=book_num,
            book_title=book_title,
            series_title=series_title,
            book_word_count=book_word_count,
            avg_words_per_chapter=avg_words_per_chapter,
            last_updated=last_updated,
            framework_id=framework_id,
            series_type_id=series_type_id,
            genre_id=genre_id,
        )
        db.session.add(plot)
        return plot

class PlotPoints(db.Model):
    __tablename__ = "plot_points"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plot_id = db.Column(db.Integer, db.ForeignKey("plot.id", ondelete="cascade"))
    plot_point_id = db.Column(db.Integer, db.ForeignKey("plotting_points.id", ondelete="cascade"))
    plot_text = db.Column(db.Text, nullable=True)
#     chapters = db.relationship("Chapter")

    def __init__(self, plot_id, plot_point_id, point_text=None):
        self.plot_id = plot_id
        self.plot_point_id = plot_point_id
        self.point_text = point_text

# class Chapter(db.Model):
#     __tablename__ = "chapters"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.Text, nullable=True)
#     ch_text = db.Column(db.Text, nullable=True)
#     plot_point_id = db.Column(db.Integer, db.ForeignKey("plot_points.id", ondelete="cascade"))
    

############## CONNECT DB ##############

def connect_db(app):
    db.app = app
    db.init_app(app)