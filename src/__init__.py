"""
A module which creates and instantiates a Flask App.
"""

import logging
from logging.handlers import RotatingFileHandler
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
    # - #
    db.init_app(app)
    #
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
    # BluePrints and RESTApi #
    #
    from src.auth import bp as auth_bp  # prevents circular import
    auth_api = Api(auth_bp)
    from src.auth.rest import UserAPI, UsersAPI  # prevents circular import
    auth_api.add_resource(UserAPI, "/api/users/<string:user_uuid>")
    auth_api.add_resource(UsersAPI, "/api/users/")
    app.register_blueprint(auth_bp, name="auth", url_prefix='/auth')
    #
    from src.errors import bp as errors_bp  # prevents circular import
    app.register_blueprint(errors_bp, name="err", url_prefix='/err')
    #
    from src.main import bp as main_bp  # prevents circular import
    app.register_blueprint(main_bp, name="main")
    #
    from src.posts import bp as posts_bp  # prevents circular import
    from src.posts.rest import PostAPI, PostsAPI  # prevents circular import
    posts_api = Api(posts_bp)
    posts_api.add_resource(PostAPI, "/api/posts/<string:post_uuid>")
    posts_api.add_resource(PostsAPI, "/api/posts/")
    app.register_blueprint(posts_bp, name="posts")
    #
    from src.quiz import bp as quiz_bp  # prevents circular import
    app.register_blueprint(quiz_bp, name="quiz")
    # - #
    # LOGGING #
    if not app.testing or app.debug:
        file_handler = RotatingFileHandler(Config.LOGS_DIR,
                                           maxBytes=10240,
                                           mode='a+',
                                           backupCount=100)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: \n'
            '%(message)s '
            '[in %(pathname)s:%(lineno)d]\n'))
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('APPLICATION HAS BEEN DEPLOYED')
    return app
