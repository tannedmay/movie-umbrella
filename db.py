import logging
import bsddb
import uuid

from utils import configure_logging
from movie_pb2 import Movie, Date, Review

_db = bsddb.btopen('movies.db', 'c')

def create(name, date_of_release, genre, duration, actors, directors, reviews):
    """add movie to movie directory

    :param name: name of film
    :param date_of_release: release date of film
    :param genre: genre of the film, one of `movie_pb2.Movie.Genre.items()`
    :param duration: duration of film in minutes
    :param actors: list of actors
    :param directors: list of directors
    :param reviews: list of reviews

    >>> import db
    >>> db.create('3 idiots', dict(month=2, day=21, year=1991),
                  Movie.DRAMA, 170, ['Amir Khan'], ['Rajkumar'],
                  [dict(rating=5,
                        date=dict(month=3, day=31, year=2016))
                  ])
    """

    try:
        _id = str(uuid.uuid4())
        date_of_release = Date(**date_of_release)
        reviews = [Review(**review) for review in reviews]

        movie = Movie(_id=_id,
                      name=name,
                      date_of_release=date_of_release,
                      genre=genre,
                      duration=duration,
                      actor=actors,
                      director=directors,
                      review=reviews)

        _db[_id] = movie.SerializeToString()
        _db.sync()
        return movie

    except Exception as exception:
         logging.error('Error while creating movie: %s' % exception.message)

def get(_id):
    try:
        movie_obj = Movie()
        movie_obj.ParseFromString(_db[_id])
    except KeyError as exception:
        raise Exception('No movie found with id: %s' % exception.message)

    return movie_obj

def search(**query_params):

    searchable_fields = ['name', 'director', 'actor', 'genre']

    def filter_movies(movie):
        for param in query_params:
            if param not in searchable_fields:
                raise Exception('{0} is not searchable parameter'.format(param))

            param_val = getattr(movie, param, None)
            if isinstance(param_val, basestring):
                if param_val != query_params[param]:
                    return False
            else:
                if query_params[param] not in param_val:
                    return False

        return True

    try:
        movies = list()
        for serialized in _db.values():
            movie_obj = Movie()
            movie_obj.ParseFromString(serialized)
            movies.append(movie_obj)

        movies = filter(filter_movies, movies)
        return movies

    except Exception as exception:
        logging.error('Error while searching/listing movie: %s' % exception.message)

def delete(_id):
    movie = get(_id)
    del _db[str(movie._id)]
    _db.sync()

    return movie

def update(_id, **new_values):
    movie = get(_id)
    for key in new_values:
        if movie.HasField(key):
            setattr(movie, key, new_values[key])
    _db[_id] = movie.SerializeToString()
    _db.sync()

    return movie
