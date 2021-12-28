from src import db


def session_create(row):
    db.session.add(row)
    db.session.commit()


def session_update():
    db.session.commit()


def session_delete(row):
    db.session.delete(row)
    db.session.commit()
