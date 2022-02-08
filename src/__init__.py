"""
A module which creates and instantiates a Flask App.
"""

import logging
from logging import FileHandler
from logging.handlers import RotatingFileHandler
import uuid
#
from flask import Flask
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
#
from config import Config

admin = Admin(name="SnakeTests", template_mode="bootstrap4")
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login_page"
login_manager.login_message_category = "info"
mail = Mail()
migrate = Migrate()


def instantiate_app(config_class=Config):  # application factory
    """
    The function creates an instance of Flask App
    while installing necessary dependencies and
    registering BLuePrints and API files.

    :param type config_class: class Config with configuration settings
    :return flask.Flask app: an instance of the Flask App
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    # ORM #
    db.init_app(app)
    # ADMIN #
    from src.auth.admin import AlteredAdminIndexView, AlteredModelView  # prevents circular import
    from src.auth.models import User  # prevents circular import
    from src.posts.models import Post  # prevents circular import
    from src.quiz.models import Option, Result, Test, Question  # prevents circular import
    admin.init_app(app, index_view=AlteredAdminIndexView())
    admin.add_view(AlteredModelView(User, db.session))
    admin.add_view(AlteredModelView(Post, db.session))
    admin.add_view(AlteredModelView(Option, db.session, category="Quiz"))
    admin.add_view(AlteredModelView(Result, db.session, category="Quiz"))
    admin.add_view(AlteredModelView(Test, db.session, category="Quiz"))
    admin.add_view(AlteredModelView(Question, db.session, category="Quiz"))
    #
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    #
    # BluePrints and RESTApi #
    from src.auth import bp as auth_bp  # prevents circular import
    auth_api = Api(auth_bp)
    from src.auth.rest import UserAPI, UsersAPI  # prevents circular import
    auth_api.add_resource(UserAPI, "/api/users/<string:user_uuid>")
    auth_api.add_resource(UsersAPI, "/api/users/")
    app.register_blueprint(auth_bp, url_prefix='/auth')
    #
    from src.errors import bp as errors_bp  # prevents circular import
    app.register_blueprint(errors_bp, url_prefix='/err')
    #
    from src.main import bp as main_bp  # prevents circular import
    app.register_blueprint(main_bp)
    #
    from src.posts import bp as posts_bp  # prevents circular import
    from src.posts.rest import PostAPI, PostsAPI  # prevents circular import
    posts_api = Api(posts_bp)
    posts_api.add_resource(PostAPI, "/api/posts/<string:post_uuid>")
    posts_api.add_resource(PostsAPI, "/api/posts/")
    app.register_blueprint(posts_bp)
    #
    from src.quiz import bp as quiz_bp  # prevents circular import
    app.register_blueprint(quiz_bp)
    # - #
    # LOGGING #
    if not (app.testing or app.debug):
        formatter = logging.Formatter(
                                      '\n%(asctime)s %(levelname)s: \n'
                                      '%(message)s '
                                      '[in %(pathname)s:%(lineno)d]'
                                     )
        file_handler = FileHandler(Config.LOGS_DIR,
                                   encoding="utf-8"
                                   )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
        #
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        app.logger.addHandler(stream_handler)
        #
        error_handler = RotatingFileHandler(Config.LOGS_WARN_DIR,
                                            encoding="utf-8",
                                            maxBytes=10240,
                                            mode='a+',
                                            backupCount=100
                                            )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.WARNING)
        app.logger.addHandler(error_handler)
        #
        app.logger.setLevel(logging.DEBUG)
        app.logger.info('APPLICATION HAS BEEN DEPLOYED')
    return app


def instantiate_test_app(config_class=Config):  # application factory
    """
    The function creates an instance of Flask App
    for debugging and testing needs only
    while installing necessary dependencies and
    registering BLuePrints and API files.

    :param type config_class: class Config with configuration settings
    :return flask.Flask app: an instance of the Flask App
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    # ORM #
    db.init_app(app)
    # ADMIN #
    from src.auth.admin import AlteredAdminIndexView, AlteredModelView  # prevents circular import
    from src.auth.models import User  # prevents circular import
    from src.posts.models import Post  # prevents circular import
    from src.quiz.models import Option, Result, Test, Question  # prevents circular import
    admin.init_app(app, index_view=AlteredAdminIndexView())
    admin.add_view(AlteredModelView(User, db.session, endpoint=f"{uuid.uuid4().hex}",))
    admin.add_view(AlteredModelView(Post, db.session, endpoint=f"{uuid.uuid4().hex}",))
    admin.add_view(AlteredModelView(Option, db.session, endpoint=f"{uuid.uuid4().hex}",
                                    category="Quiz"))
    admin.add_view(AlteredModelView(Result, db.session, endpoint=f"{uuid.uuid4().hex}",
                                    category="Quiz"))
    admin.add_view(AlteredModelView(Test, db.session, endpoint=f"{uuid.uuid4().hex}",
                                    category="Quiz"))
    admin.add_view(AlteredModelView(Question, db.session, endpoint=f"{uuid.uuid4().hex}",
                                    category="Quiz"))
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    #
    # BluePrints and RESTApi #
    from src.auth import bp as auth_bp  # prevents circular import
    auth_api = Api(auth_bp)
    from src.auth.rest import UserAPI, UsersAPI  # prevents circular import
    auth_api.add_resource(UserAPI, "/api/users/<string:user_uuid>", endpoint=f"{uuid.uuid4().hex}")
    auth_api.add_resource(UsersAPI, "/api/users/", endpoint=f"{uuid.uuid4().hex}")
    app.register_blueprint(auth_bp, url_prefix='/auth')
    #
    from src.errors import bp as errors_bp  # prevents circular import
    app.register_blueprint(errors_bp, url_prefix='/err')
    #
    from src.main import bp as main_bp  # prevents circular import
    app.register_blueprint(main_bp)
    #
    from src.posts import bp as posts_bp  # prevents circular import
    from src.posts.rest import PostAPI, PostsAPI  # prevents circular import
    posts_api = Api(posts_bp)
    posts_api.add_resource(PostAPI, "/api/posts/<string:post_uuid>", endpoint=f"{uuid.uuid4().hex}")
    posts_api.add_resource(PostsAPI, "/api/posts/", endpoint=f"{uuid.uuid4().hex}")
    app.register_blueprint(posts_bp)
    #
    from src.quiz import bp as quiz_bp  # prevents circular import
    app.register_blueprint(quiz_bp)
    return app
