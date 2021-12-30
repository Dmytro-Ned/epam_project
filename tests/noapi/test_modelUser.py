import os
import unittest
#
from sqlalchemy.exc import DataError
#
from src import instantiate_app, db
from src.auth.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')


class UserModelCase(unittest.TestCase):

    def setUp(self):
        app = instantiate_app(TestConfig)
        self.context = app.app_context()
        self.context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.context.pop()

    def test_password_hashing(self):
        test_user = User()
        test_user.encrypt_password('hashed_value')
        self.assertTrue(test_user.verify_password('hashed_value'))
        self.assertFalse(test_user.verify_password('some_password'))

    def test_user_add(self):
        test_user2 = User(username="testUser", email="test@user.com")
        test_user2.encrypt_password("hashed_test_pass")
        db.session.add(test_user2)
        db.session.commit()
        self.assertIn(test_user2, User.query.all())


if __name__ == '__main__':
    unittest.main(verbosity=2)
