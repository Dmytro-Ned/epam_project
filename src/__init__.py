from flask import Flask
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
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
    # BluePrints #
    from src.auth import bp as auth_bp  # prevents circular import
    app.register_blueprint(auth_bp, url_prefix='/auth')
    #
    from src.errors import bp as errors_bp  # prevents circular import
    app.register_blueprint(errors_bp, url_prefix='/err')
    #
    from src.main import bp as main_bp  # prevents circular import
    app.register_blueprint(main_bp)
    #
    from src.posts import bp as posts_bp  # prevents circular import
    app.register_blueprint(posts_bp)
    #
    from src.quiz import bp as quiz_bp  # prevents circular import
    app.register_blueprint(quiz_bp)
    # - #
    return app
