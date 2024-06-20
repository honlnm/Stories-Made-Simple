from app import app
from models import db
from unittest import TestCase

class AuthTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True
        cls.app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stories_test'
        with cls.app.app_context():
            db.create_all()
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup(self):
        with self.app.test_client() as client:
            res = client.post('/auth/signup', data={'username': 'testuser', 'password': 'abc123', 'email': 'testuser@gmail.com'})

            self.assertEqual(res.status_code, 201)

    def test_login(self):
        with self.app.test_client() as client:
            res = client.post('/auth/token', data={'username': 'testuser', 'password': 'abc123'})

            self.assertEqual(res.status_code, 200)

