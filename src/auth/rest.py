from string import punctuation
#
from flask import abort
from flask_restful import Resource, reqparse, marshal_with, fields
from flask_login import current_user
#
from sqlalchemy.exc import DataError

from main.service import session_create, session_update, session_delete
from src.auth.models import User


class UserCommonAPI(Resource):
    post_user = reqparse.RequestParser()
    post_user.add_argument('first_name', type=str, help="first name field", default="")
    post_user.add_argument('last_name', type=str, help="last name field", default="")
    post_user.add_argument('username', type=str, help="username field is required", required=True)
    post_user.add_argument('email', type=str, help="email field is required", required=True)
    post_user.add_argument('password', type=str, help="password field is required", required=True)

    put_user = reqparse.RequestParser()
    put_user.add_argument('first_name', type=str, help="first name field is required", required=True)
    put_user.add_argument('last_name', type=str, help="last name field is required", required=True)
    put_user.add_argument('username', type=str, help="username field is required", required=True)
    put_user.add_argument('email', type=str, help="email field is required is required", required=True)

    patch_user = reqparse.RequestParser()
    patch_user.add_argument('first_name', type=str, help="first name field")
    patch_user.add_argument('last_name', type=str, help="last name field")
    patch_user.add_argument('username', type=str, help="username field")
    patch_user.add_argument('email', type=str, help="email field")
    # password cannot be changed via REST (security measures)

    object_fields = {
        "uuid": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
        "username": fields.String,
        "email": fields.String,
    }

    def get_user(self, user_uuid):
        try:
            user = User.query.filter_by(uuid=user_uuid).first()
            if not user:
                return abort(404, "A user with this UUID does not exist")
            return user
        except DataError:  # in case UUID is input in inept format
            abort(400, "Bad request. Inept UUID format")

    def verify_authorization(self):
        if current_user.is_anonymous:
            return abort(401, "Unauthorized. Log In")

    def verify_identity(self, user):
        if current_user.uuid != user.uuid:
            return abort(403, "Forbidden. Bad credentials")

    def validate_input(self, username, email, password, first_name, last_name):
        attributes = [username, email, password, first_name, last_name]
        for attr in attributes:
            if attr and not isinstance(attr, str):
                return abort(415, "Unsupported media type. All fields must be string")
        if username:
            self.validate_username(username)
        if email:
            self.validate_email(email)
        if password and (8 > len(password) or len(password) > 30):
            return abort(411, "Length required. password must be 8-30 characters")
        if first_name and (2 > len(first_name) or len(first_name) > 20):
            return abort(411, "Length required. first_name must be 2-20 characters")
        if last_name and (2 > len(last_name) or len(last_name) > 40):
            return abort(411, "Length required. last_name must be 2-40 characters")

    def validate_username(self, username):
        if 2 > len(username) or len(username) > 20:
            return abort(411, "Length required. username must be 2-20 characters")
        for char in username:
            forbidden_chars = punctuation + " "
            if char in forbidden_chars:
                return abort(406, f"Not acceptable. Forbidden characters: {forbidden_chars}")
        if username.lower() in ['admin', 'administrator']:
            return abort(406, "Not acceptable. Forbidden name")
        user = User.query.filter_by(username=username).first()
        if user:
            return abort(406, "Not acceptable. A user with this username already exists")

    def validate_email(self, email):
        if 2 > len(email) or len(email) > 30:
            return abort(411, "Length required. email must be 2-30 characters")
        if " " in email or "@" not in email or "." not in email.split("@")[-1] or \
                (len(email.split("@")[-1]) < 5):
            return abort(406, "Not acceptable. Wrong email format")
        user = User.query.filter_by(email=email).first()
        if user:
            return abort(406, "Not acceptable. A user with this email already exists")


class UserAPI(UserCommonAPI):

    @marshal_with(UserCommonAPI.object_fields, envelope="user")
    def get(self, user_uuid):
        super().verify_authorization()
        user = super().get_user(user_uuid)
        if current_user.is_superuser:  # admin may view any profile
            return user
        super().verify_identity(user)  # other users may view their own profiles
        return user

    @marshal_with(UserCommonAPI.object_fields)
    def put(self, user_uuid):
        super().verify_authorization()
        user = super().get_user(user_uuid)
        super().verify_identity(user)  # users may edit only their own profiles
        #
        args = super().put_user.parse_args(strict=True)
        super().validate_input(args["username"],
                               args["email"],
                               "********",  # password modification is not supported with PUT
                               args["first_name"],
                               args["last_name"]
                               )
        user.first_name = args["first_name"]
        user.last_name = args["last_name"]
        user.username = args["username"]
        user.email = args["email"]
        session_update()
        return user

    @marshal_with(UserCommonAPI.object_fields)
    def patch(self, user_uuid):
        super().verify_authorization()
        user = super().get_user(user_uuid)
        super().verify_identity(user)  # users may edit only their own profiles
        #
        args = super().patch_user.parse_args(strict=True)
        if not (args.get("first_name", None) or args.get("last_name", None) or
                args.get("username", None) or args.get("email", None)):
            return abort(406, f"PATCH method must implement the modification "
                              f"of at list one field of an object: {list(args)}")
        super().validate_input(args["username"],
                               args["email"],
                               "********",  # password modification is not supported with PATCH
                               args["first_name"],
                               args["last_name"]
                               )
        if args.get("first_name", None):
            user.first_name = args["first_name"]
        if args.get("last_name", None):
            user.last_name = args["last_name"]
        if args.get("username", None):
            user.username = args["username"]
        if args.get("email", None):
            user.email = args["email"]
        session_update()
        return user

    def delete(self, user_uuid):
        super().verify_authorization()
        user = super().get_user(user_uuid)
        super().verify_identity(user)
        return "This feature is not implemented"  # removal of users is typically unacceptable


class UsersAPI(UserCommonAPI):

    @marshal_with(UserCommonAPI.object_fields)
    def get(self):
        super().verify_authorization()
        if not current_user.is_superuser:
            return current_user    # users may view only their own profiles
        return User.query.all()    # admin may view every profile

    @marshal_with(UserCommonAPI.object_fields)
    def post(self):
        super().verify_authorization()
        if not current_user.is_superuser:  # only admin may create new users through REST
            return abort(403, "Forbidden. Bad credentials")
        user = User()
        args = super().post_user.parse_args()
        super().validate_input(args["username"],
                               args["email"],
                               args["password"],
                               args["first_name"],
                               args["last_name"]
                               )
        user.first_name = args["first_name"]
        user.last_name = args["last_name"]
        user.username = args["username"]
        user.email = args["email"]
        user.encrypt_password(args["password"])
        session_create(user)
        return User.query.all()
