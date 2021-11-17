"""
Module directors yang berisi fungsi untuk endpoint REST API
"""

from flask import make_response, abort
from config import db
from models import Directors, DirectorsSchema, Movies


def read_all():
    """
    Fungsi ini me-return semua director
    Fungsi akan terpanggil melalui url /api/directors
    dengan method get
    """
    # Query untuk semua directors diambil 10 data
    directors = Directors.query.order_by(Directors.id).limit(10)

    # Serialize list dari hasil query
    directors_schema = DirectorsSchema(many=True)
    data = directors_schema.dump(directors)
    return data


def read_one(directors_id):
    """
    Fungsi ini me-return director sesuai directors_id 
    yang diberikan melalui url /api/directors/{directors_id}
    dengan method get
    Fungsi juga akan me-return status 200 jika ada datanya
    dan akan melakukan abort dan status 404 jika tidak ada datanya
    """
    # Query join directors dan movies
    directors = (
        Directors.query.filter(Directors.id == directors_id)
        .outerjoin(Movies)
        .one_or_none()
    )

    # Cek directors apakah ada
    if directors is not None:

        # Serialize list dari hasil query
        directors_schema = DirectorsSchema()
        data = directors_schema.dump(directors)
        return data

    # Return 404 jika tidak ada directors nya
    else:
        abort(404, f"Director not found for Id: {directors_id}")


def create(directors):
    """
    Fungsi ini akan membuat data director baru melalui
    url /api/directors/{directors_id}/movies dengan method post
    Request body nya berupa object directors tanpa atribut id dan movies
    Fungsi akan me-return data director yang berhasil dibuat dan status code 201
    dan fungsi akan melakukan abort dan me-return status 409 jika sudah ada data yang sama persis
    """
    # Ambil data yang dikirim untuk dicek
    name = directors.get("name")
    gender = directors.get("gender")
    uid = directors.get("uid")
    department = directors.get("department")

    # Object untuk cek apakah ada director dengan data yang sama
    existing_director = (
        Directors.query.filter(Directors.name == name)
        .filter(Directors.gender == gender)
        .filter(Directors.uid == uid)
        .filter(Directors.department == department)
        .one_or_none()
    )

    # Cek apakah sudah ada director dengan data yang sama
    if existing_director is None:

        # Create director menggunakan schema
        schema = DirectorsSchema()
        new_directors = schema.load(directors, session=db.session)

        # Add data ke database
        db.session.add(new_directors)
        db.session.commit()

        # Ambil data yang berhasil di-create
        data = schema.dump(new_directors)

        return data, 201

    # Jika sudah ada directors dengan data yang sama
    else:
        abort(409, f"Director {name} with {uid} in {department} department exists already")


def update(directors_id, directors):
    """
    Fungsi ini akan melakukan update data director sesuai dengan directors_id yang diberikan melalui
    url /api/directors/{directors_id} dengan method put
    Request body nya berupa object directors tanpa atribut id dan movies
    Fungsi akan me-return data director yang berhasil diupdate dan status code 200
    dan fungsi akan melakukan abort dan status 404 jika data tidak ditemukan
    """
    # Query untuk get data director sesuai id
    update_directors = Directors.query.filter(
        Directors.id == directors_id
    ).one_or_none()

    # Cek apakah ada datanya
    if update_directors is not None:

        # Ambil datanya dan diubah dalam bentuk db object
        schema = DirectorsSchema()
        update = schema.load(directors, session=db.session)

        # Set id director sesuai dengan yang mau di-update
        update.id = update_directors.id

        # Update datanya
        db.session.merge(update)
        db.session.commit()

        # Ambil data yang berhasil di-update
        data = schema.dump(update_directors)

        return data, 200

    # Return 404 jika tidak ada directors nya
    else:
        abort(404, f"Director not found for Id: {directors_id}")


def delete(directors_id):
    """
    Fungsi ini akan melakukan delete data director dengan directors_id sesuai dengan yang diberikan melalui
    url /api/directors/{directors_id} dengan method delete
    Fungsi akan me-return message dan status code 200 jika berhasil di-delete
    dan fungsi akan melakukan abort dan status 404 jika data tidak ditemukan
    """
    # Query untuk get data director sesuai id
    directors = Directors.query.filter(Directors.id == directors_id).one_or_none()

    # Cek apakah ada datanya
    if directors is not None:
        db.session.delete(directors)
        db.session.commit()
        return make_response(f"Director with id {directors_id} deleted", 200)

    # Return 404 jika tidak ada directors nya
    else:
        abort(404, f"Director not found for Id: {directors_id}")
