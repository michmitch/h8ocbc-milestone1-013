"""
Module movies yang berisi fungsi untuk endpoint REST API
"""

from flask import make_response, abort
from config import db
from models import Directors, Movies, MoviesSchema


def read_all():
    """
    Fungsi ini me-return semua movies beserta detail directornya
    Fungsi akan terpanggil melalui url /api/directors/movies
    dengan method get
    """
    # Query untuk semua movies diambil 10 data
    movies = Movies.query.order_by(Movies.id).limit(10)

    # Serialize list dari hasil query
    movies_schema = MoviesSchema(many=True)
    data = movies_schema.dump(movies)
    return data


def read_one(directors_id, movies_id):
    """
    Fungsi ini me-return movie sesuai movie_id dan directors_id 
    yang diberikan melalui url /api/directors/{directors_id}/movies/{movies_id}
    dengan method get
    """
    # Query untuk movie sesuai director_id dan movie_id
    movies = (
        Movies.query.join(Directors, Directors.id == Movies.director_id)
        .filter(Directors.id == directors_id)
        .filter(Movies.id == movies_id)
        .one_or_none()
    )

    # Cek movie apakah ada di database
    if movies is not None:
        movies_schema = MoviesSchema()
        data = movies_schema.dump(movies)
        return data, 200

    # Return 404 jika tidak ketemu movie nya
    else:
        abort(404, f"Movies not found for Id: {movies_id}")


def create(directors_id, movies):
    """
    This function creates a new note related to the passed in person id.
    :param person_id:       Id of the person the note is related to
    :param note:            The JSON containing the note data
    :return:                201 on success
    """
    # get the parent person
    directors = Directors.query.filter(Directors.id == directors_id).one_or_none()

    # Was a person found?
    if directors is None:
        abort(404, f"Director not found for Id: {directors}")

    # Create a note schema instance
    schema = MoviesSchema()
    new_movies = schema.load(movies, session=db.session)

    # Add the note to the person and database
    directors.movies.append(new_movies)
    db.session.commit()

    # Serialize and return the newly created note in the response
    data = schema.dump(new_movies)

    return data, 201


def update(directors_id, movies_id, movies):
    """
    This function updates an existing note related to the passed in
    person id.
    :param person_id:       Id of the person the note is related to
    :param note_id:         Id of the note to update
    :param content:            The JSON containing the note data
    :return:                200 on success
    """
    update_movies = (
        Movies.query.filter(Directors.id == directors_id)
        .filter(Movies.id == movies_id)
        .one_or_none()
    )

    # Did we find an existing note?
    if update_movies is not None:

        # turn the passed in note into a db object
        schema = MoviesSchema()
        update = schema.load(movies, session=db.session)

        # Set the id's to the note we want to update
        update.director_id = update_movies.director_id
        update.id = update_movies.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated note in the response
        data = schema.dump(update_movies)

        return data, 200

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Movie not found for Id: {movies_id}")


def delete(directors_id, movies_id):
    """
    This function deletes a note from the note structure
    :param person_id:   Id of the person the note is related to
    :param note_id:     Id of the note to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the note requested
    movies = (
        Movies.query.filter(Directors.id == directors_id)
        .filter(Movies.id == movies_id)
        .one_or_none()
    )

    # did we find a note?
    if movies is not None:
        db.session.delete(movies)
        db.session.commit()
        return make_response(
            f"Movie {movies_id} deleted", 200
        )

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Movie not found for Id: {movies_id}")