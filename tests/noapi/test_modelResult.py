import os
import unittest
#
from src import instantiate_test_app, db
from src.auth.models import User
from src.quiz.models import Result, Test
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
                              "postgresql://postgres:postgres@localhost:5433/testflaskapp"


class TestModelCase(unittest.TestCase):

    def setUp(self):
        self.app = instantiate_test_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.user = User(username="testUser", email="test@user.com")
        self.user.encrypt_password("test_pass")
        self.test_test = Test(title="Custom Title", description="Custom Test")
        db.session.add(self.test_test)
        db.session.add(self.user)
        db.session.commit()
        self.test_result = Result(user_id=self.user.id, test_id=self.test_test.id)
        db.session.add(self.test_result)
        db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_result_add(self):
        test_result = Result(user_id=self.user.id, test_id=self.test_test.id)
        db.session.add(test_result)
        db.session.commit()
        self.assertIn(test_result, Result.query.all())

    def test_result_update(self):
        self.assertEqual(self.test_result.num_correct_answers, 0)
        self.test_result.num_correct_answers = 2
        db.session.commit()
        self.assertEqual(self.test_result.num_correct_answers, 2)

    def test_result_delete(self):
        self.assertIn(self.test_result, Result.query.all())
        db.session.delete(self.test_result)
        db.session.commit()
        no_result = Result.query.first()
        self.assertIsNone(no_result)
