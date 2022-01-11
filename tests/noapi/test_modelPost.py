import os
import unittest
#
from sqlalchemy.exc import DataError
from flask_login import login_user
#
from src import instantiate_test_app, db
from src.auth.models import User
from src.posts.models import Post
from src.quiz.models import Test
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
                              "postgresql://postgres:postgres@localhost:5433/testflaskapp"


class UserModelCase(unittest.TestCase):

    def setUp(self):
        self.app = instantiate_test_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.test_user = User(username="testUser", email="test@user.com")
        self.test_user.encrypt_password("hashed_test_pass")
        self.test_test = Test(title="Custom Title", description="Custom Test")
        db.session.add(self.test_user)
        db.session.add(self.test_test)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_post_add(self):
        test_post = Post(title="Test Topic", content="Lorem Ipsum",
                         user_id=self.test_user.id, test_id=self.test_test.id)
        db.session.add(test_post)
        db.session.commit()
        self.assertIn(test_post, Post.query.all())

    def test_post_update(self):
        new_post = Post(title="Test Topic", content="Lorem Ipsum",
                        user_id=self.test_user.id, test_id=self.test_test.id)
        db.session.add(new_post)
        db.session.commit()
        test_post = Post.query.filter_by(content="Lorem Ipsum").first()
        test_post.title = "Altered Topic"
        db.session.commit()
        self.assertEqual(test_post.title, "Altered Topic")

    def test_post_delete(self):
        new_post = Post(title="Test Topic", content="Lorem Ipsum",
                        user_id=self.test_user.id, test_id=self.test_test.id)
        db.session.add(new_post)
        db.session.commit()
        test_post = Post.query.filter_by(content="Lorem Ipsum").first()
        self.assertEqual(test_post.title, "Test Topic")
        db.session.delete(test_post)
        db.session.commit()
        no_post = Post.query.filter_by(content="Lorem Ipsum").first()
        self.assertIsNone(no_post)

    def test_orm_len_constraints(self):
        new_post = Post(title="Long Test Topic:"
                              "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                              "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...",
                        content="Lorem Ipsum",
                        user_id=self.test_user.id,
                        test_id=self.test_test.id)
        db.session.add(new_post)
        self.assertRaises(DataError, db.session.commit)

    def test_post_create_page(self):
        with self.app.test_request_context():
            login_user(User.query.get(1))
        response = self.client.get("/posts/create")
        self.assertEqual(response.status_code, 302)
        response = self.client.post('auth/login',
                                    data=dict(
                                             title="Test Topic",
                                             content="Lorem Ipsum",
                                             user_id=self.test_user.id,
                                             test_id=self.test_test.id
                                            )
                                    )
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
