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

    def test_01_signup(self):
        with self.app.test_client() as client:
            res = client.post('/auth/signup', json={'username': 'testuser', 'password': 'abc123', 'email': 'testuser@gmail.com'}, content_type='application/json')

            self.assertEqual(res.status_code, 201)

    def test_02_signup_validation(self):
        with self.app.test_client() as client:
            res = client.post('/auth/signup', json={'username': 'testuser', 'email': 'testuser@gmail.com'}, content_type='application/json')

            self.assertEqual(res.status_code, 400)
            self.assertIn(b"Missing required fields", res.data)

    def test_03_invalid_signup(self):
        with self.app.test_client() as client:
            res = client.post('/auth/signup', json={'username': 'testuser', 'password': 'abc123', 'email': 'testuser@gmail.com'}, content_type='application/json')

            self.assertEqual(res.status_code, 400)
            self.assertIn(b"Username or email already taken", res.data)

    def test_04_login(self):
        with self.app.test_client() as client:
            res = client.post('/auth/token', json={'username': 'testuser', 'password': 'abc123'}, content_type='application/json')

            self.assertEqual(res.status_code, 200)

    def test_05_invalid_login(self):
        with self.app.test_client() as client:
            res = client.post('/auth/token', json={'username': 'testuser', 'password': 'invalid'}, content_type='application/json')

            self.assertEqual(res.status_code, 401)
            self.assertIn(b"Invalid username or password", res.data)
