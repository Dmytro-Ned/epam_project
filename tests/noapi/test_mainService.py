import os
import unittest
#
from src import instantiate_test_app, db
from src.auth.models import User
from src.main.service import session_create, session_update, session_delete
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
                              "postgresql://postgres:postgres@localhost/testflaskapp"


class TestModelCase(unittest.TestCase):

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

    def test_main_page(self):
        request = self.client.get("/")
        self.assertEqual(request.status_code, 200)

    def test_db_services(self):
        user = User(username="test", email="test@mail")
        user.encrypt_password("testpassword")
        session_create(user)
        self.assertEquals(User.query.first().email, "test@mail")
        user.first_name, user.last_name = "Mark", "Wonderwill"
        session_update()
        self.assertEquals(User.query.first().first_name, "Mark")
        session_delete(user)
        no_user = User.query.first()
        self.assertNotIn(no_user, User.query.all())

    def test_error_pages(self):
        get_404 = self.client.get("/notexists/page")
        self.assertEqual(get_404.status_code, 404)


# if __name__ == "__main__":
#     unittest.main(verbosity=2)
