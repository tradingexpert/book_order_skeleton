from typing import Tuple, Dict, Union

from flask import Blueprint, Request, request, jsonify
from jsonschema import validate
from sqlalchemy import func

from bookapp.models import db, User, BookRequest, Book, get_or_create_user, get_or_create_request


api = Blueprint("api", "bookapp")

# TODO: This could be separted out, moved into an untracked file (or along the first section of the view - decorator)
add_schema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string', 'pattern': '[a-z0-9\._%+!$&*=^|~#%{}/\-]+@([a-z0-9\-]+\.){1,}([a-z]{2,22})'},
        'title': {'type': 'string'}
    },
    'required': ['email', 'title']
}

email_only_schema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string', 'pattern': '[a-z0-9\._%+!$&*=^|~#%{}/\-]+@([a-z0-9\-]+\.){1,}([a-z]{2,22})'}
    },
    'required': ['email']
}


def check_if_json_correct(request_in: Request, schema: Dict) -> Tuple[Dict[str, str], int]:
    """
    Checks if the request contains a json, and if that json is valid based on the provided schema

    :param request_in: originating request object
    :param schema: validation schema
    :return: Tuple of dictionary of error, and http error code
        A dictionary containing an error key, and the exception details + the http error code (only errors)
    """
    got = request_in.get_json()
    if not got:
        return {"error": "The request does not contain a json"}, 400
    try:
        validate(got, schema=schema)
    except Exception as e:
        return {"error": str(e)}, 422
    # All is fine, 0 allows error code to be checked as quasi boolean
    return got, 0


# TODO: multiple requests are not supported as per the document (but could easily be added)
@api.route('/request', methods=['POST'])
def add_request():
    try:
        got, failure = check_if_json_correct(request, schema=add_schema)
        if failure:
            return jsonify(got), failure
        # Check if the title exist in the db (Other than checking with uppercase, no further logic here now)
        book = db.session.query(Book).filter(func.upper(Book.title) == got['title'].upper()).first()
        if not book:
            return jsonify({"status": "We do not currently have this book available"}), 204
        user = get_or_create_user(email=got["email"])
        # Now we have the user and the book
        book_req, return_code = get_or_create_request(user_id=user.id, book_id=book.id)
        return jsonify(
            {"email": user.email, "title": book.title, "id": book_req.id, "timestamp": book_req.timestamp}), return_code

    except Exception as e:  # This can be extended to deal with specific errors (let's return a json with 500)
        return jsonify({"error": str(e)}), 500


@api.route('/request/', methods=['GET'])
@api.route('/request/<int:id>', methods=['GET'])
def get_request(id: int = None):
    try:
        # The assumption I have made is that we still provide an email in json
        got, failure = check_if_json_correct(request, schema=email_only_schema)
        if failure:
            return jsonify(got), failure
        if not id:
            resource_list = []
            user = db.session.query(User).filter(User.email == got['email']).first()
            book_reqs = db.session.query(BookRequest).filter(BookRequest.user_id == user.id).all()
            for book_req in book_reqs:
                book = db.session.query(Book).filter(Book.id == book_req.book_id)
                resource_list.append(
                    {"email": user.email, "title": book.title, "id": book_req.id, "timestamp": book_req.timestamp})
            return jsonify(resource_list), 200
        else:
            book_req = db.session.query(BookRequest).filter(BookRequest.id == id).first()
            if not book_req:
                return jsonify({"error": "The id requested does not exist"}), 404
            book = db.session.query(Book).filter(Book.id == book_req.book_id).first()
            return jsonify(
                {"email": got['email'], "title": book.title, "id": book_req.id, "timestamp": book_req.timestamp}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/request/<int:id>', methods=['DELETE'])
def delete_request(id: int):
    try:
        got, failure = check_if_json_correct(request, schema=email_only_schema)
        if failure:
            return jsonify(got), failure
        book_req = db.session.query(BookRequest).filter(BookRequest.id == id).first()
        if not book_req:
            return jsonify({"error": "We cannot delete a request that doesn't exist"}), 404
        else:
            db.session.query(BookRequest).filter(BookRequest.id == id).delete()
            db.session.commit()
            return {}, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
