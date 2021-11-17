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
    Fungsi juga akan me-return status 200 jika ada datanya
    dan akan melakukan abort dan status 404 jika tidak ada datanya
    """
    # Query join movies dan directors
    movies = (
        Movies.query.join(Directors, Directors.id == Movies.director_id)
        .filter(Directors.id == directors_id)
        .filter(Movies.id == movies_id)
        .one_or_none()
    )

    # Cek movies apakah ada
    if movies is not None:
        movies_schema = MoviesSchema()
        data = movies_schema.dump(movies)
        return data, 200

    # Return 404 jika tidak ada movies nya
    else:
        abort(404, f"Movies not found for Id: {movies_id}")


def create(directors_id, movies):
    """
    Fungsi ini akan membuat data movies baru dengan directors_id sesuai dengan yang diberikan melalui
    url /api/directors/{directors_id}/movies dengan method post
    Request body nya berupa object movies tanpa atribut director_id dan id
    Fungsi akan me-return data movies yang berhasil dibuat dan status code 201
    """
    # Ambil data director untuk dicek
    directors = Directors.query.filter(Directors.id == directors_id).one_or_none()

    # Return 404 jika tidak ada directors
    if directors is None:
        abort(404, f"Director not found for Id: {directors}")

    # # Create movies menggunakan schema
    schema = MoviesSchema()
    new_movies = schema.load(movies, session=db.session)

    # Add data ke database
    directors.movies.append(new_movies)
    db.session.commit()

    # Ambil data yang berhasil di-create
    data = schema.dump(new_movies)

    return data, 201


def update(directors_id, movies_id, movies):
    """
    Fungsi ini akan melakukan update data movies dengan directors_id dan movies_id sesuai dengan yang diberikan melalui
    url /api/directors/{directors_id}/movies/{movies_id} dengan method put
    Request body nya berupa object movies tanpa atribut director_id dan id
    Fungsi akan me-return data movies yang berhasil diupdate dan status code 200
    dan fungsi akan melakukan abort dan status 404 jika data tidak ditemukan
    """
    # Query untuk get data movies sesuai director_id dan id
    update_movies = (
        Movies.query.filter(Directors.id == directors_id)
        .filter(Movies.id == movies_id)
        .one_or_none()
    )

    # Cek apakah ada datanya
    if update_movies is not None:

        # Ambil datanya dan diubah dalam bentuk db object
        schema = MoviesSchema()
        update = schema.load(movies, session=db.session)

        # Set director_id dan id sesuai dengan yang mau di-update
        update.director_id = update_movies.director_id
        update.id = update_movies.id

        # Update datanya
        db.session.merge(update)
        db.session.commit()

        # Ambil data yang berhasil di-update
        data = schema.dump(update_movies)

        return data, 200

    # Return 404 jika tidak ada movies nya
    else:
        abort(404, f"Movie not found for Id: {movies_id}")


def delete(directors_id, movies_id):
    """
    Fungsi ini akan melakukan delete data movies dengan directors_id dan movies_id sesuai dengan yang diberikan melalui
    url /api/directors/{directors_id}/movies/{movies_id} dengan method delete
    Fungsi akan me-return message dan status code 200 jika berhasil di-delete
    dan fungsi akan melakukan abort dan status 404 jika data tidak ditemukan
    """
    # Query untuk get data movies sesuai director_id dan id
    movies = (
        Movies.query.filter(Directors.id == directors_id)
        .filter(Movies.id == movies_id)
        .one_or_none()
    )

    # Cek apakah ada datanya
    if movies is not None:
        db.session.delete(movies)
        db.session.commit()
        return make_response(
            f"Movie {movies_id} deleted", 200
        )

    # Return 404 jika tidak ada movies nya
    else:
        abort(404, f"Movie not found for Id: {movies_id}")
