import os
import unittest
#
from src import instantiate_test_app, db
from src.auth.models import User
from src.quiz.models import Result, Test, Question
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
        self.test_test = Test(title="Custom Title", description="Custom Test")
        db.session.add(self.test_test)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_test_add(self):
        test_test = Test(title="Custom Title 2", description="Custom Test 2")
        db.session.add(test_test)
        db.session.commit()
        self.assertIn(test_test, Test.query.all())

    def test_test_update(self):
        self.assertEqual(self.test_test.title, "Custom Title")
        self.test_test.title = "Altered Title"
        db.session.commit()
        self.assertEqual(self.test_test.title, "Altered Title")

    def test_test_delete(self):
        self.assertIn(self.test_test, Test.query.all())
        db.session.delete(self.test_test)
        db.session.commit()
        no_test = Test.query.filter_by(title="Custom Title").first()
        self.assertIsNone(no_test)

    def test_num_questions(self):
        question = Question(test_id=self.test_test.id)
        db.session.add(question)
        db.session.commit()
        self.assertEqual(self.test_test.get_num_questions(), 1)

    def test_get_results(self):
        self.assertEqual(self.test_test.get_num_questions(), 0)
        self.assertEqual(self.test_test.get_best_result(), 0)
        self.assertEqual(self.test_test.get_last_result(), 0)
        user = User(username="testUser", email="test@user.com")
        user.encrypt_password("test_pass")
        db.session.add(user)
        db.session.commit()
        question = Question(text="Blah Blah", test_id=self.test_test.id)
        result_1 = Result(user_id=user.id, test_id=self.test_test.id)
        result_2 = Result(user_id=user.id, test_id=self.test_test.id, num_correct_answers=3)
        db.session.add(question)
        db.session.add(result_1)
        db.session.add(result_2)
        db.session.commit()
        self.assertEqual(self.test_test.get_num_questions(), 1)
        # self.assertEqual(self.test_test.get_best_result(), result_2)  # TODO: LOGIN
        # self.assertEqual(self.test_test.get_last_result(), result_2)

    def test_tests_list_page(self):
        response = self.client.get("/tests/")
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main(verbosity=2)
