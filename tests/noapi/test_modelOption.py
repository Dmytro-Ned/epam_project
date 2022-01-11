import os
import unittest
#
from src import instantiate_test_app, db
from src.quiz.models import Option, Test, Question
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
        db.session.add(self.test_test)
        db.session.add(self.test_question)
        db.session.commit()
        self.test_option = Option(text="Sample Text", question_id=self.test_question.id)
        db.session.add(self.test_option)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_option_add(self):
        test_option = Option(text="Sample Text 2", question_id=self.test_question.id)
        db.session.add(test_option)
        db.session.commit()
        self.assertIn(test_option, Option.query.all())

    def test_option_update(self):
        self.assertEqual(self.test_option.text, "Sample Text")
        self.test_option.text = "Sample Text Altered"
        db.session.commit()
        self.assertEqual(self.test_option.text, "Sample Text Altered")

    def test_option_delete(self):
        self.assertIn(self.test_option, Option.query.all())
        db.session.delete(self.test_option)
        db.session.commit()
        no_test = Option.query.first()
        self.assertIsNone(no_test)

