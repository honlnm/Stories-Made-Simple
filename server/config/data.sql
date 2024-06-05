CREATE TABLE plotting_framworks (
    framework_id SERIAL PRIMARY KEY,
    framework_name TEXT NOT NULL,
    framework_description TEXT NOT NULL,
    num_of_plot_points INTEGER NOT NULL
)

CREATE TABLE series_type (
    series_type_id SERIAL PRIMARY KEY,
    series_type_name TEXT NOT NULL,
    series_type_num_of_books INTEGER NOT NULL,
    series_type_avg_word_count INTEGER NOT NULL
)

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    user_created_at TIMESTAMP NOT NULL,
    user_last_updated_at TIMESTAMP NOT NULL
)

CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name TEXT NOT NULL,
    genre_description TEXT NOT NULL,
    genre_avg_word_count INTEGER NOT NULL
)

CREATE TABLE plotting_point (
    plot_point_id SERIAL PRIMARY KEY,
    framework_id INTEGER NOT NULL,
    plot_step INTEGER NOT NULL,
    percent_of_story NUMBER NOT NULL,
    plot_point_description TEXT NOT NULL,
    FOREIGN KEY (framework_id) REFERENCES plotting_framworks(framework_id)
)

CREATE TABLE plot_series (
    plot_series_id SERIAL PRIMARY KEY,
    framework_id INTEGER NOT NULL,
    series_type_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    num_of_books INTEGER NOT NULL,
    series_title TEXT NOT NULL,
    plot_series_last_updated TIMESTAMP NOT NULL,
    FOREIGN KEY (framework_id) REFERENCES plotting_framworks(framework_id),
    FOREIGN KEY (series_type_id) REFERENCES series_type(series_type_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
)

CREATE TABLE book_plot (
    book_plot_id SERIAL PRIMARY KEY,
    plot_series_id INTEGER NOT NULL,
    book_title TEXT NOT NULL,
    desired_book_total_word_count INTEGER NOT NULL,
    FOREIGN KEY (plot_series_id) REFERENCES plot_series(plot_series_id)
)

CREATE TABLE book_plot_points (
    sbook_plot_point_id SERIAL PRIMARY KEY,
    plot_point_id INTEGER NOT NULL,
    book_plot_id INTEGER NOT NULL,
    desired_words_per_chapter INTEGER NOT NULL,
    FOREIGN KEY (plot_point_id) REFERENCES plotting_point(plot_point_id),
    FOREIGN KEY (book_plot_id) REFERENCES book_plot(book_plot_id)
)