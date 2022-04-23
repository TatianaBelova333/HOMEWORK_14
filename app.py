import utils
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config["JSON_SORT_KEYS"] = False


content_rating = {'children': ('G',), 'family': ('G', 'PG', 'PG-13'), 'adult': ('R', 'NC-17')}
database_path = 'netflix.db'


@app.route('/movie/<title>')
def search_by_title(title):
    movie = utils.search_by_movie_title(database_path, title, limit=1)
    return jsonify(movie)


@app.route('/movie/<int:start_year>/to/<int:end_year>')
def search_by_period(start_year, end_year):
    movies = utils.search_by_period(database_path, start_year, end_year, limit=100)
    return jsonify(movies)


@app.route('/rating/<age_group>')
def search_by_age_group(age_group):
    movies = utils.search_by_content_rating(database_path, content_rating.get(age_group))
    return jsonify(movies)


@app.route('/genre/<genre>')
def search_by_genre(genre):
    movies = utils.search_by_genre(database_path, genre, limit=10)
    return jsonify(movies)


if __name__ == '__main__':
    app.run()



