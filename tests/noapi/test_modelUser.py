import os
import unittest
#
from sqlalchemy.exc import DataError, IntegrityError, PendingRollbackError
#
from src import instantiate_test_app, db
from src.auth.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")


class UserModelCase(unittest.TestCase):

    def setUp(self):
        self.app = instantiate_test_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_full_name(self):
        test_user = User(first_name="John", last_name="Doe")
        self.assertEqual(test_user.full_name, "John Doe")
        self.assertNotEqual(test_user.full_name, "William Johnson")

    def test_password_hash(self):
        test_user = User()
        test_user.encrypt_password('hashed_value')
        self.assertTrue(test_user.verify_password('hashed_value'))
        self.assertFalse(test_user.verify_password('some_password'))

    def test_user_add(self):
        test_user = User(username="testUser", email="test@user.com")
        test_user.encrypt_password("hashed_test_pass")
        db.session.add(test_user)
        db.session.commit()
        self.assertIn(test_user, User.query.all())

    def test_user_update(self):
        new_user = User(username="testUser", email="test@user.com")
        new_user.encrypt_password("hashed_test_pass")
        db.session.add(new_user)
        db.session.commit()
        test_user = User.query.filter_by(username="testUser").first()
        test_user.first_name = "Test"
        test_user.last_name = "Case"
        db.session.commit()
        self.assertEqual(test_user.full_name, "Test Case")

    def test_user_delete(self):
        new_user = User(username="testUser", email="test@user.com")
        new_user.encrypt_password("hashed_test_pass")
        db.session.add(new_user)
        db.session.commit()
        test_user = User.query.filter_by(username="testUser").first()
        self.assertEqual(test_user.username, "testUser")
        db.session.delete(test_user)
        db.session.commit()
        no_user = User.query.filter_by(username="testUser").first()
        self.assertIsNone(no_user)

    def test_orm_len_constraints(self):
        new_user = User(username="testUser", email="test@user.com")
        new_user.encrypt_password("hashed_test_pass")
        db.session.add(new_user)
        db.session.commit()
        test_user = User.query.filter_by(username="testUser").first()
        with self.assertRaises(PendingRollbackError):
            test_user.first_name = "HuitzilopochtliTlaloc"
            self.assertRaises(DataError, db.session.commit)
            test_user.last_name = "Wolfenschlegelsteinmeirshausenbergerdorff"
            self.assertRaises(DataError, db.session.commit)
            test_user.username = "test2LongUsernameUser"
            self.assertRaises(DataError, db.session.commit)

    def test_orm_unique_constraints(self):
        new_user = User(username="testUser", email="test@user.com")
        new_user.encrypt_password("hashed_test_pass")
        db.session.add(new_user)
        db.session.commit()
        same_user = User(username="testUser", email="test@user.com")
        same_user.encrypt_password("hashed_test_pass")
        db.session.add(same_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_register_page(self):
        response = self.client.get("auth/register")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("auth/register",
                                    data={"username": "testUser",
                                          "email": "test@user.com",
                                          "password_hash": "hashed_test_pass",
                                          "g_recaptcha_response": True},
                                    follow_redirects=True
                                    )
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get("/auth/login")
        self.assertEqual(response.status_code, 200)
        new_user = User(username="testUser", email="test@user.com")
        new_user.encrypt_password("hashed_test_pass")
        db.session.add(new_user)
        db.session.commit()
        response = self.client.post('auth/login',
                                    data=dict(
                                             username="testUser",
                                             password="hashed_test_pass"
                                            )
                                    )
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
