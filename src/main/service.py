"""
The module encapsulates functions
for basic CRUD operation with data structures.
"""

from src import db


def session_create(row):
    """
    Implements CREATE CRUD operation.

    :param SQLAlchemy().Model row: a newly created instance
                                   of an SQL ORM model
    """
    db.session.add(row)
    db.session.commit()


def session_update():
    """
    Implements UPDATE CRUD operation.
    """
    db.session.commit()


def session_delete(row):
    """
    Implements DELETE CRUD operation.

    :param SQLAlchemy().Model row: an existing instance
                                   of an SQL ORM model
                                   to be removed from the DB
    """
    db.session.delete(row)
    db.session.commit()
