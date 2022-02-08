import os
import unittest
#
from flask import current_app
from flask_login import login_user
#
from src import instantiate_test_app, db
from src.auth.models import User
from src.posts.models import Post
from src.quiz.models import Test
from config import Config


class TestConfig(Config):
    TESTING = True
    LOGIN_DISABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")


class UserApiCase(unittest.TestCase):

    def setUp(self):
        self.app = instantiate_test_app(TestConfig)
        self.client = self.app.test_client()
        with self.client:
            self.app_context = self.app.app_context()
            self.app_context.push()
        db.create_all()
        self.test_admin = User(username="admn", email="admin@istrat.or")
        self.test_admin.encrypt_password("hashed_super_pass")
        self.test_admin.is_superuser = True
        self.test_user = User(username="testUser", email="test@user.com")
        self.test_user.encrypt_password("hashed_test_pass")
        self.test_test = Test(title="Custom Title", description="Custom Test")

        db.session.add(self.test_admin)
        db.session.add(self.test_user)
        db.session.add(self.test_test)
        db.session.commit()
        self.test_post = Post(title="Test Topic", content="Lorem Ipsum",
                              user_id=self.test_user.id, test_id=self.test_test.id)
        db.session.add(self.test_post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_posts(self):
        test_post = Post(title="Test Topic 2", content="Lorem Ipsum 2",
                         user_id=self.test_user.id, test_id=self.test_test.id)
        db.session.add(test_post)
        db.session.commit()
        api_get = self.client.get('/api/posts/')
        self.assertEqual(api_get.status_code, 401)

    def test_post_posts(self):
        api_post = self.client.post('api/posts/',
                                    data={"title": "REST TOPIC 2",
                                          "content": "REST CONTENT 2",
                                          "user_id": "0",
                                          "test_id": "0"
                                          }
                                    )
        self.assertEqual(api_post.status_code, 401)
        with self.client:
            login_user(self.test_admin)
            api_post = self.client.get('/auth/api/users/')
        self.assertEqual(api_post.status_code, 200)

    def test_get_post(self):
        api_post = self.client.get(f'/api/posts/{self.test_post.uuid}')
        self.assertEqual(api_post.status_code, 401)

    def test_patch_post(self):
        api_patch = self.client.put(f'/api/posts/{self.test_post.uuid}',
                                    data={"content": "ALTERED"}
                                    )
        self.assertEqual(api_patch.status_code, 401)

    def test_put_post(self):
        api_put = self.client.put(f'/api/posts/{self.test_post.uuid}',
                                  data={"title": "REST TOPIC Alt",
                                        "content": "REST CONTENT Alt"
                                        }
                                  )
        self.assertEqual(api_put.status_code, 401)

    def test_delete_post(self):
        api_delete = self.client.delete(f'/api/posts/{self.test_post.uuid}')
        self.assertEqual(api_delete.status_code, 401)


if __name__ == '__main__':
    unittest.main(verbosity=2)
