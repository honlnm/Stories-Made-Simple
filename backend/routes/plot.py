from flask import (
    Blueprint,
    session,
    request,
    jsonify,
    g
)
from sqlalchemy.exc import IntegrityError
from models import db, PlottingPoint, Plot, PlotPoints, PlottingFramework

plot_bp = Blueprint("plot", __name__, url_prefix="/plot")

def get_plotting_point_ids_for_framework(framework_id):
    plotting_points = PlottingPoint.query.filter_by(framework_id=framework_id).all()
    return [point.id for point in plotting_points]
    
@plot_bp.route("<int:user_id>/create", methods=["POST"])
def create_plot(user_id, plot_id):
    if user_id != g.user.id:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    num_of_books=data.get('num_of_books')
    book_num=data.get('book_num')
    book_title=data.get('book_title')
    series_title=data.get('series_title')
    book_word_count=data.get('book_word_count')
    avg_words_per_chapter=data.get('avg_words_per_chapter')
    last_updated=data.get('last_updated')
    framework_id=data.get('framework_id')
    series_type_id=data.get('series_type_id')
    genre_id=data.get('genre_id')

    if not data or not num_of_books or not book_num or not book_title or not series_title or not book_word_count or not avg_words_per_chapter or not framework_id or not series_type_id or not genre_id:
        return jsonify({"error": "Missing required fields"}), 400
    
    if not  last_updated:
        return jsonify({"error": "Missing 'last updated' field, please contact site administrator."}), 500

    plot = Plot.create(
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
    db.session.commit()

    plotting_point_ids_arr = get_plotting_point_ids_for_framework(framework_id)
    for plot_point_id in plotting_point_ids_arr:
        point = PlotPoints(plot_id, plot_point_id)
        db.session.add(point)
    db.session.commit()

    return jsonify({"message": "Plot created successfully", "plot": {"plot_id": plot.id}}), 201


@plot_bp.route("/<int:user_id>/<int:plot_id>")
def show_plot(user_id, plot_id):
    plots_for_user = Plot.query.filter_by(user_id=user_id).all()
    plot_ids = [plot.id for plot in plots_for_user]
    if user_id != g.user.id:
        return jsonify({"error": "Unauthorized"}), 401
    if plot_id not in plot_ids:
        return jsonify({"error": "Plot does not exist for user"}), 404
    plot = Plot.query.get_or_404(plot_id)
    return jsonify({"plot": {"id": plot.id, 
                             "book_num": plot.book_num,
                             "book_title": plot.book_title,
                             "series_title": plot.series_title,
                             "book_word_count": plot.book_word_count,
                             "avg_words_per_chapter": plot.avg_words_per_chapter,
                             "last_updated": plot.last_updated,
                             "framework_id": plot.framework_id,
                             "series_type_id": plot.series_type_id,
                             "user_id": plot.user_id,
                             "genre_id": plot.genre_id}}), 201


@plot_bp.route("/<int:user_id>/<int:plot_id>/delete", methods=["POST"])
def delete_plot(user_id, plot_id):
    plots_for_user = Plot.query.filter_by(user_id=user_id).all()
    plot_ids = [plot.id for plot in plots_for_user]
    if user_id != g.user.id:
        return jsonify({"error": "Unauthorized"}), 401
    if plot_id not in plot_ids:
        return jsonify({"error": "Plot does not exist for user"}), 404
    plot = Plot.query.get_or_404(plot_id)
    db.session.delete(plot)
    db.session.commit()