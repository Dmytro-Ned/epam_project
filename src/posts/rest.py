"""
The module implements REST-friendly API
for CRUD operations with instances of "Post" ORM model.
"""

from flask import abort
from flask_restful import Resource, reqparse, marshal_with, fields
from flask_login import current_user
#
from sqlalchemy.exc import DataError

from src.main.service import session_update, session_delete
from src.posts.models import Post


class PostCommonAPI(Resource):
    """
    General API class with features
    used by all its children.

    Fields:
        - put_post: a request parser with args for PUT method
        - patch_post: a request parser with args for PATCH method
        - object_field: a hash table of object fields representable in API
    """
    put_post = reqparse.RequestParser()
    put_post.add_argument('title', type=str, help="title field required", required=True)
    put_post.add_argument('content', type=str, help="content field required", required=True)

    patch_post = reqparse.RequestParser()
    patch_post.add_argument('title', type=str, help="title of the post")
    patch_post.add_argument('content', type=str, help="content of the post")

    object_fields = {
        "uuid": fields.String,
        "title": fields.String,
        "content": fields.String,
        "user": fields.String(attribute="author.username"),
        "test": fields.String(attribute="test.title"),
    }

    def get_post(self, post_uuid):
        """
        Fetches a post from "post" table
        by UUID if the uuid is correct and
        a post with such uuid exists in the table.
        Aborts execution in case of wrong data input.

        :param UUID post_uuid: uuid of the post
        :return Post post: an instance of "Post" ORM model
        """
        try:
            post = Post.query.filter_by(uuid=post_uuid).first()
            if not post:
                return abort(404, "A post with this UUID does not exist")
            return post
        except DataError:  # in case UUID is input in inept format
            abort(400, "Bad request. Inept UUID format")

    def verify_authorization(self):
        """
        Verifies if client is authorized to interact with REST API.
        Aborts execution otherwise.
        """
        if current_user.is_anonymous:
            return abort(401, "Unauthorized. Log In")

    def verify_authorship(self, post):
        """
        Verifies if client is authorized to interact with REST API.
        Aborts execution otherwise.

        :param Post post: an instance of ORM "Post" model
        """
        if current_user.uuid != post.author.uuid:
            return abort(403, "Forbidden. Bad credentials")


class PostAPI(PostCommonAPI):
    """
    REST API class for interactions with rows of the table "post".
    (RUD/CRUD operations).

    methods: get, put, patch, delete
    """

    @marshal_with(PostCommonAPI.object_fields, envelope="post")
    def get(self, post_uuid):
        """
        REST API GET method.

        :param UUID post_uuid: UUID of a post
        :return Post post: an instance of "Post" ORM model
        """
        super().verify_authorization()
        post = super().get_post(post_uuid)
        if current_user.is_superuser:  # admin may view all posts
            return post
        super().verify_authorship(post)  # other users may view their own posts
        return post

    @marshal_with(PostCommonAPI.object_fields)
    def put(self, post_uuid):
        """
        REST API PUT method.

        :param UUID post_uuid: UUID of a post
        :return Post post: an instance of "Post" ORM model
        """
        super().verify_authorization()
        post = super().get_post(post_uuid)
        super().verify_authorship(post)  # only authors may edit their own posts
        #
        args = super().put_post.parse_args(strict=True)
        post.title = args["title"]
        post.content = args["content"]
        session_update()
        return post

    @marshal_with(PostCommonAPI.object_fields)
    def patch(self, post_uuid):
        """
        REST API PATCH method.

        :param UUID post_uuid: UUID of a post
        :return Post post: an instance of "Post" ORM model
        """
        super().verify_authorization()
        post = super().get_post(post_uuid)
        super().verify_authorship(post)  # only authors may edit their own posts
        #
        args = super().patch_post.parse_args(strict=True)
        if not (args.get("title", None) or args.get("content", None)):
            return abort(406, f"PATCH method must implement the modification "
                              f"of at list one field of an object: {list(args)}")
        if args.get("title", None):
            post.title = args["title"]
        if args.get("content", None):
            post.content = args["content"]
        session_update()
        return post

    def delete(self, post_uuid):
        """
        REST API DELETE method.

        :param UUID post_uuid: UUID of a post
        :return str: status hint
        """
        super().verify_authorization()
        post = super().get_post(post_uuid)
        super().verify_authorship(post)  # only authors may edit their own posts
        #
        session_delete(post)
        return "deletion successful", 200


class PostsAPI(PostCommonAPI):
    """
    REST API class for interactions with the whole table "post".
    (CR/CRUD operations).

    methods: get, post
    """

    @marshal_with(PostCommonAPI.object_fields)
    def get(self):
        """
        REST API GET method.

        :return list: all existing instances of "Post" ORM model
        """
        super().verify_authorization()
        if current_user.is_superuser:
            posts = Post.query.all()
        else:
            posts = Post.query.filter_by(user_id=current_user.id).all()
        return posts

    def post(self):
        """
        REST API POST method.
        Aborts execution if an attempt of access
        is made by a non-admin user.

        :return post Post: a recently created instance of "Post" ORM model
        """
        super().verify_authorization()
        if not current_user.is_superuser:
            return abort(403, "Forbidden. Bad credentials")
        return "This feature is not implemented"  # FEEDBACK THROUGH REST API is inconvenient
                                                  # TODO: test links names - digits; ADMIN won't leave feedback
