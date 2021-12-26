from datetime import datetime
from uuid import uuid4
#
from sqlalchemy.dialects.postgresql import UUID
#
from src import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid4, index=True, unique=True)  # PgSQL
    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # do not put parenthesis: current time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # prevents user deletion by Admin
    test_id = db.Column(db.Integer, db.ForeignKey('test.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"Post({self.title}, {self.post_date})"
