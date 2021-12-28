from flask import abort
from flask_restful import Resource, reqparse, marshal_with, fields
from flask_login import current_user
#
from sqlalchemy.exc import DataError

from main.service import session_update, session_delete
from src.posts.models import Post


class PostCommonAPI(Resource):
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
        try:
            post = Post.query.filter_by(uuid=post_uuid).first()
            if not post:
                return abort(404, "A post with this UUID does not exist")
            return post
        except DataError:  # in case UUID is input in inept format
            abort(400, "Bad request. Inept UUID format")

    def verify_authorization(self):
        if current_user.is_anonymous:
            return abort(401, "Unauthorized. Log In")

    def verify_authorship(self, post):
        if current_user.uuid != post.author.uuid:
            return abort(403, "Forbidden. Bad credentials")


class PostAPI(PostCommonAPI):

    @marshal_with(PostCommonAPI.object_fields, envelope="post")
    def get(self, post_uuid):
        super().verify_authorization()
        post = super().get_post(post_uuid)
        if current_user.is_superuser:  # admin may view all posts
            return post
        super().verify_authorship(post)  # other users may view their own posts
        return post

    @marshal_with(PostCommonAPI.object_fields)
    def put(self, post_uuid):
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
        super().verify_authorization()
        post = super().get_post(post_uuid)
        super().verify_authorship(post)  # only authors may edit their own posts
        #
        session_delete(post)
        return "deletion successful", 200


class PostsAPI(PostCommonAPI):

    @marshal_with(PostCommonAPI.object_fields)
    def get(self):
        super().verify_authorization()
        if current_user.is_superuser:
            posts = Post.query.all()
        else:
            posts = Post.query.filter_by(user_id=current_user.id).all()
        return posts

    def post(self):
        super().verify_authorization()
        if not current_user.is_superuser:
            return abort(403, "Forbidden. Bad credentials")
        return "This feature is not implemented"  # FEEDBACK THROUGH REST API is inconvenient
                                                  # TODO: test links names - digits; ADMIN won't leave feedback
