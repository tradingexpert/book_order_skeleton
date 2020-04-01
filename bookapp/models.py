from typing import Tuple
from datetime import datetime

from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# TODO: If these entities are not to even be queried separately, I would revert the normalization
class Book(db.Model):
    """Books by title"""
    __tablename__ = 'books'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(255), index=True, unique=True)


class User(db.Model):
    """Users that have made requests"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), index=True, unique=True)


# TODO: Will not enforce referential integrity as it stands, despite GDPR requirements
class BookRequest(db.Model):
    """Requests for books"""
    __tablename__ = 'bookrequests'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(User.id), primary_key=False, nullable=False)
    book_id = db.Column(db.Integer, ForeignKey(Book.id), primary_key=False, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


def get_or_create_user(email: str) -> User:
    """
    Gets an existing user, or creates one if it 'not exists'

    :param email: The email to look up user
    :return: The existing/created user
    """
    user = db.session.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()
    return user


def get_or_create_request(user_id: int, book_id: int) -> Tuple[BookRequest, int]:
    """
    Gets a request or creates one if it doesn't exist, based on the user id and book id

    :param user_id: id of User
    :param book_id: id of Book
    :return:
        Tuple of the book request and the resulting http status code
        (reflecting whether new or existing request is returned)
    """
    book_req = db.session.query(BookRequest).filter(BookRequest.user_id == user_id,
                                                    BookRequest.book_id == book_id).first()
    return_code = 200       # For already processed requests
    if not book_req:
        book_req = BookRequest(user_id=user_id, book_id=book_id, timestamp=datetime.now())
        db.session.add(book_req)
        db.session.commit()
        return_code = 201   # For newly created records
    return book_req, return_code
