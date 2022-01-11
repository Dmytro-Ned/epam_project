import os
import unittest
#
from src import instantiate_test_app, db
from src.auth.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    LOGIN_DISABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
                              "postgresql://postgres:postgres@localhost:5433/testflaskapp"


class UserApiCase(unittest.TestCase):

    def setUp(self):
        self.app = instantiate_test_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.test_admin = User(username="admn", email="admin@istrat.or")
        self.test_admin.encrypt_password("hashed_super_pass")
        self.test_admin.is_superuser = True
        self.test_user_1 = User(username="testUser", email="test@user.com")
        self.test_user_1.encrypt_password("hashed_test_pass")
        self.test_user_2 = User(username="testUser2", email="test2@user.com")
        self.test_user_2.encrypt_password("hashed_test_pass")
        db.session.add(self.test_admin)
        db.session.add(self.test_user_1)
        db.session.add(self.test_user_2)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_users(self):
        api_get = self.client.get('/auth/api/users/')
        self.assertEqual(api_get.status_code, 401)

    def test_post_users(self):
        api_post = self.client.post('/auth/api/users/',
                                    data={"username": "testUser",
                                          "email": "test@user.com",
                                          "password_hash": "hashed_test_pass"
                                          }
                                    )
        self.assertEqual(api_post.status_code, 401)

    def test_get_user(self):
        api_get = self.client.get(f'/auth/api/users/{self.test_admin.uuid}')
        self.assertEqual(api_get.status_code, 401)

    def test_patch_user(self):
        api_patch = self.client.patch(f'/auth/api/users/{self.test_admin.uuid}',
                                      data={"username": "testUserMod"}
                                      )
        self.assertEqual(api_patch.status_code, 401)

    def test_put_user(self):
        api_put = self.client.put(f'/auth/api/users/{self.test_admin.uuid}',
                                  data={"username": "testUserMod",
                                        "email": "test@userMod.com",
                                        }
                                  )
        self.assertEqual(api_put.status_code, 401)

    def test_delete_user(self):
        api_delete = self.client.delete(f'/auth/api/users/{self.test_admin.uuid}')
        self.assertEqual(api_delete.status_code, 401)


if __name__ == '__main__':
    unittest.main(verbosity=2)
