"""
This is the people module and supports all the REST actions for the
people data
"""

from flask import make_response, abort
from config import db
from models import Directors, DirectorsSchema, Movies


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    directors = Directors.query.order_by(Directors.id).limit(10)

    # Serialize the data for the response
    directors_schema = DirectorsSchema(many=True)
    data = directors_schema.dump(directors)
    return data


def read_one(directors_id):
    """
    This function responds to a request for /api/people/{person_id}
    with one matching person from people
    :param person_id:   Id of person to find
    :return:            person matching id
    """
    # Build the initial query
    directors = (
        Directors.query.filter(Directors.id == directors_id)
        .outerjoin(Movies)
        .one_or_none()
    )

    # Did we find a person?
    if directors is not None:

        # Serialize the data for the response
        directors_schema = DirectorsSchema()
        data = directors_schema.dump(directors)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Director not found for Id: {directors_id}")


def create(directors):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    name = directors.get("name")
    gender = directors.get("gender")
    uid = directors.get("uid")
    department = directors.get("department")



    existing_director = (
        Directors.query.filter(Directors.name == name)
        .filter(Directors.gender == gender)
        .filter(Directors.uid == uid)
        .filter(Directors.department == department)
        .one_or_none()
    )

    # Can we insert this person?
    if existing_director is None:

        # Create a person instance using the schema and the passed in person
        schema = DirectorsSchema()
        new_directors = schema.load(directors, session=db.session)

        # Add the person to the database
        db.session.add(new_directors)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_directors)

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(409, f"Director {name} with {uid} in {department} department exists already")


def update(directors_id, directors):
    """
    This function updates an existing person in the people structure
    :param person_id:   Id of the person to update in the people structure
    :param person:      person to update
    :return:            updated person structure
    """
    # Get the person requested from the db into session
    update_directors = Directors.query.filter(
        Directors.id == directors_id
    ).one_or_none()

    # Did we find an existing person?
    if update_directors is not None:

        # turn the passed in person into a db object
        schema = DirectorsSchema()
        update = schema.load(directors, session=db.session)

        # Set the id to the person we want to update
        update.id = update_directors.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_directors)

        return data, 200

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Director not found for Id: {directors_id}")


def delete(directors_id):
    """
    This function deletes a person from the people structure
    :param person_id:   Id of the person to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    directors = Directors.query.filter(Directors.id == directors_id).one_or_none()

    # Did we find a person?
    if directors is not None:
        db.session.delete(directors)
        db.session.commit()
        return make_response(f"Director with id {directors_id} deleted", 200)

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Director not found for Id: {directors_id}")