import os
#
from dotenv import load_dotenv


basedir = os.path.abspath(os.getcwd())
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    FLASK_APP = os.environ.get('FLASK_APP') or 'app.py'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    #
    FLASK_ADMIN_SWATCH = os.environ.get('FLASK_ADMIN_SWATCH') or 'cerulean'
    #
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://server:servere@localhost/flaskapp'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'quiz.db') # TODO: remove
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Don't send a signal to the app every time a change is a made in the DB.
    #
    BUNDLE_ERRORS = True  # RESTFullAPI ReqParse
    #
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #
    TABLES_PER_PAGE = 10
    POSTS_PER_PAGE = 10
    #
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_DATA_ATTRS = {'size': 'compact', 'theme': 'light'}
