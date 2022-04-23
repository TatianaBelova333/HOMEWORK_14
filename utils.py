import sqlite3
import json

# Структура таблицы
# -----------------------
# show_id — id тайтла
# type — фильм или сериал
# title — название
# director — режиссер
# cast — основные актеры
# country — страна производства
# date_added — когда добавлен на Нетфликс
# release_year — когда выпущен в прокат
# rating — возрастной рейтинг
# duration — длительность
# duration_type — минуты или сезоны
# listed_in — список жанров и подборок
# description — краткое описание
# -----------------------
database = 'netflix.db'


def convert_into_list_of_dict(keys: list, data: list):
    converted_data = []
    for item in data:
        item_dict = dict(zip(keys, item))
        converted_data.append(item_dict)
    return converted_data


def connect_to_sqlite_database(database_path, sqlite_query, params):
    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        data_raw = cursor.execute(sqlite_query, params).fetchall()
    return data_raw


def search_by_movie_title(database_path, movie_title: str, limit: int):
    keys = ['title', 'country', 'release_year', 'genre', 'description']
    movie_title = '%' + movie_title + '%'
    params = (movie_title, limit)
    # Sorting by length to return the title closest to the pattern
    sqlite_query = """
                         SELECT title, 
                                country, 
                                release_year, 
                                listed_in, 
                                description               
                         FROM netflix
                         WHERE `type` = 'Movie' AND title LIKE ?
                         ORDER BY LENGTH(title), release_year DESC 
                         LIMIT ?
                """
    movie_raw = connect_to_sqlite_database(database_path, sqlite_query, params)
    movie_info = convert_into_list_of_dict(keys, movie_raw)
    return movie_info


def search_by_period(database_path, start_year: int, end_year: int, limit: int):
    keys = ['title', 'release_year']
    params = (start_year, end_year, limit)
    sqlite_query = """
            SELECT title, release_year
            FROM netflix
            WHERE `type` = 'Movie' AND release_year BETWEEN ? AND ?
            ORDER BY release_year
            LIMIT ?
        """
    movies_raw = connect_to_sqlite_database(database_path, sqlite_query, params)
    movies_info = convert_into_list_of_dict(keys, movies_raw)
    return movies_info


def search_by_content_rating(database_path, age_group: tuple):
    keys = ['title', 'rating', 'description']
    sqlite_query = """
            SELECT title, rating, description
            FROM netflix
            WHERE rating COLLATE NOCASE IN (%s)
            ORDER BY rating, release_year DESC
        """ % ','.join('?' * len(age_group))
    movies_raw = connect_to_sqlite_database(database_path, sqlite_query, age_group)
    movies_list = convert_into_list_of_dict(keys, movies_raw)
    return movies_list


def search_by_genre(database_path, genre: str, limit: int):
    keys = ['title', 'description']
    genre = '%' + genre + '%'
    params = (genre, limit)
    sqlite_query = """
            SELECT title, description
            FROM netflix
            WHERE `type` = 'Movie' AND listed_in LIKE ?
            ORDER BY release_year DESC
            LIMIT ?
        """
    movies_raw = connect_to_sqlite_database(database_path, sqlite_query, params)
    movies_info = convert_into_list_of_dict(keys, movies_raw)
    return movies_info


def search_by_type_year_genre(database_path, content_type: str, release_year: int, genre: str, limit=10):
    keys = ['title', 'description']
    genre = '%' + genre + '%'
    params = (content_type, release_year, genre, limit)
    sqlite_query = """
            SELECT title, description
            FROM netflix
            WHERE `type` = ? AND release_year = ? AND listed_in LIKE ? 
            ORDER BY release_year DESC
            LIMIT ?
        """
    movies_raw = connect_to_sqlite_database(database_path, sqlite_query, params)
    movies_info = convert_into_list_of_dict(keys, movies_raw)
    movies_info_json = json.dumps(movies_info, ensure_ascii=False, indent=4)
    return movies_info_json


def search_for_fellow_actors(database_path, actor_1: str, actor_2: str):
    if not isinstance(actor_1, str) or not isinstance(actor_2, str):
        raise TypeError('Имена актеров должны быть string')
    actor_1_sql_str = '%' + actor_1 + '%'
    actor_2_sql_str = '%' + actor_2 + '%'
    params = (actor_1_sql_str, actor_2_sql_str)
    sqlite_query = """
            SELECT `cast`
            FROM netflix
            WHERE `cast` LIKE ? AND `cast` LIKE ?
        """
    movie_casts = connect_to_sqlite_database(database_path, sqlite_query, params)
    fellow_actors = {}
    for cast in movie_casts:
        for actor in cast[0].split(', '):
            if actor != actor_1 and actor != actor_2:
                fellow_actors[actor] = fellow_actors.get(actor, 0) + 1
    multiple_fellow_actors = list(filter(lambda x: x[1] > 2, fellow_actors.items()))
    multiple_fellow_actors_res = [item[0] for item in multiple_fellow_actors]
    return multiple_fellow_actors_res



