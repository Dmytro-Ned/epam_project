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
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
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
    results = db.relationship('Result', backref='user', cascade="all, delete-orphan", lazy=True, passive_deletes=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def encrypt_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password=password).decode()

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=180):
        serializer = Serializer(current_app.config['SECRET_KEY'],
                                expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User({self.username}, {self.email})"
