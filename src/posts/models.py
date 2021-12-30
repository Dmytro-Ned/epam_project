"""
This module contains SQL ORM model for "Post" instances.
"""

from datetime import datetime
from uuid import uuid4
#
from sqlalchemy.dialects.postgresql import UUID
#
from src import db


class Post(db.Model):
    """
    An ORM class which represents SQL table "post".

    Fields: id, uuid, title, content, post date, author, related test.
    """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid4, index=True, unique=True)  # PgSQL
    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # do not put parenthesis: current time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # prevents user deletion by Admin
    test_id = db.Column(db.Integer, db.ForeignKey('test.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        """
        Readable representation of an instance.

        :return str: title and date of publication of the post
        """
        return f"Post({self.title}, {self.post_date})"
