"""
This module contains SQL ORM model for "User" instances.
"""

from uuid import uuid4
#
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.dialects.postgresql import UUID
#
from src import bcrypt, db, login_manager


@login_manager.user_loader   # must be implemented to use the 'flask_login' functions
def load_user(user_id):
    """
    This function substitutes 4 typical methods
    arising during login/logout procedures.

    :param int user_id: primary key of a db User instance
    :return User: and instance of User class by id
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    An ORM class which represents SQL table "user".

    Fields: id, uuid, first name, last name, username, email, image, hashed password,
            superuser flag, related posts rel.,related test results rel.
    """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid4, index=True, unique=True)  # PgSQL
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(40))
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    image = db.Column(db.String(20), unique=False, nullable=False, default='default.png')
    password_hash = db.Column(db.String(60), unique=False, nullable=False)
    is_superuser = db.Column(db.Boolean, unique=False, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)  # prevents user deletion by Admin
    results = db.relationship('Result', backref='user', cascade="all, delete-orphan",
                              lazy=True, passive_deletes=True)

    @property
    def full_name(self):
        """
        Returns user's fullname as a property.

        :return str: full name of a user
        """
        return f"{self.first_name} {self.last_name}"

    def encrypt_password(self, password):
        """
        Encrypts an input password via bcrypt coding.

        :param str password: input non-hashed password
        """
        self.password_hash = bcrypt.generate_password_hash(password=password).decode()

    def verify_password(self, password):
        """
        Verifies if an input access password corresponds
        to an encrypted (hashed) password of the user.

        :param str password: an input password sequence
        :return bool: an indicator of correspondence
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=180):
        """
        Generates a unique token for password change access.

        :param int expires_sec: time period during which token is valid
        :return str: a decoded token
        """
        serializer = Serializer(current_app.config['SECRET_KEY'],
                                expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
        Verifies a user before password change.
        Returns a user if verification passes
        and None in case it fails.

        :param str token: unique token to verify a user
        :return User/NoneType: a User instance by id/None
        """
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id']
        except Exception:  # pylint: disable=W0703
            return None
        return User.query.get(user_id)

    def __repr__(self):
        """
        Readable representation of an instance.

        :return str: username and email of a user
        """
        return f"User({self.username}, {self.email})"
