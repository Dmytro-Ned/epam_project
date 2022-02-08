import os
import unittest
#
from src import instantiate_test_app, db
from src.quiz.models import Test, Question
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
        self.test_test = Test(title="Custom Title", description="Custom Test")
        db.session.add(self.test_test)
        db.session.commit()
        self.test_question = Question(text="QInit", test_id=self.test_test.id)
        db.session.add(self.test_question)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_question_add(self):
        test_question = Question(text="Q1", test_id=self.test_test.id)
        db.session.add(test_question)
        db.session.commit()
        self.assertIn(test_question, Question.query.all())

    def test_question_update(self):
        self.assertEqual(self.test_question.text, "QInit")
        self.test_question.text = "QAltered"
        db.session.commit()
        self.assertEqual(self.test_question.text, "QAltered")

    def test_question_delete(self):
        self.assertIn(self.test_question, Question.query.all())
        db.session.delete(self.test_question)
        db.session.commit()
        no_question = Question.query.filter_by(text="QInit").first()
        self.assertIsNone(no_question)


if __name__ == '__main__':
    unittest.main(verbosity=2)
