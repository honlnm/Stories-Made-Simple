from unittest.mock import patch
from flask import g
from app import app
from models import db, User
from seed import seed_data
from unittest import TestCase

class PlotTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True
        cls.app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stories_test'
        with cls.app.app_context():
            db.session.query(User).delete()
            db.session.commit()
            db.create_all()
            seed_data()
            cls.client.post('/auth/signup', json={'username': 'testuser', 'password': 'abc123', 'email': 'testuser@gmail.com'}, content_type='application/json')
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.mock_user = User.query.filter_by(username="testuser").first()

    def tearDown(self):
        self.app_context.pop()

    def test_01_create_unauthorized(self):
        response = self.client.post(f"plot/999/create", json={
            "num_of_books": 1,
            "book_num": 1,
            "book_title": "book title",
            "series_title": "series title",
            "book_word_count": 100000,
            "avg_words_per_chapter": 2500,
            "framework_id": 1,
            "series_type_id": 1,
            "genre_id": 1,  
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Unauthorized", response.data)

    @patch('flask.g')
    def test_02_create_authorized(self, mock_g):
        mock_g.user = self.mock_user
        response = self.client.post(f"plot/{self.mock_user.id}/create", json={
            "num_of_books": 1,
            "book_num": 1,
            "book_title": "book title",
            "series_title": "series title",
            "book_word_count": 100000,
            "avg_words_per_chapter": 2500,
            "framework_id": 1,
            "series_type_id": 1,
            "genre_id": 1,  
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Plot created successfully", response.data)

    @patch('flask.g')
    def test_03_show_list_unauthorized(self, mock_g):
        response = self.client.get(f"plot/999")
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Unauthorized", response.data)

    @patch('flask.g')
    def test_04_show_list_authorized(self, mock_g):
        mock_g.user = self.mock_user
        response = self.client.get(f"plot/{self.mock_user.id}")
        self.assertEqual(response.status_code, 200)

    @patch('flask.g')
    def test_05_show_plot_unauthorized(self, mock_g):
        response = self.client.get(f"plot/999/1")
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Unauthorized", response.data)
    
    @patch('flask.g')
    def test_06_show_plot_authorized(self, mock_g):
        mock_g.user = self.mock_user
        response = self.client.get(f"plot/{self.mock_user.id}/1")
        self.assertEqual(response.status_code, 200)
    
    @patch('flask.g')
    def test_07_edit_plot_unauthorized(self, mock_g):
        response = self.client.post(f"plot/999/1/edit", json={
            "num_of_books": 1,
            "book_num": 1,
            "book_title": "changed book title",
            "series_title": "series title",
            "book_word_count": 100000,
            "avg_words_per_chapter": 2500,
            "framework_id": 1,
            "series_type_id": 1,
            "genre_id": 1,
            "plot_points": [{
                "id": 1,
                "plot_text": "This is the text for plot point 1."
            },
            {
                "id": 2,
                "plot_text": "This is the text for pot point 2."
            }]
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Unauthorized", response.data)
    
    @patch('flask.g')
    def test_08_edit_plot_authorized(self, mock_g):
        mock_g.user = self.mock_user
        response = self.client.post(f"plot/{self.mock_user.id}/1/edit", json={
            "num_of_books": 1,
            "book_num": 1,
            "book_title": "changed book title",
            "series_title": "series title",
            "book_word_count": 100000,
            "avg_words_per_chapter": 2500,
            "framework_id": 1,
            "series_type_id": 1,
            "genre_id": 1,
            "plot_points": [{
                "id": 1,
                "plot_text": "This is the text for plot point 1."
            },
            {
                "id": 2,
                "plot_text": "This is the text for pot point 2."
            }]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Plot and plot points updated successfully", response.data)
    
    @patch('flask.g')
    def test_09_delete_plot_unauthorized(self, mock_g):
        response =  self.client.post(f"plot/999/1/delete")
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Unauthorized", response.data)
    
    @patch('flask.g')
    def test_10_delete_plot_authorized(self, mock_g):
        mock_g.user = self.mock_user
        response = self.client.post(f"plot/{self.mock_user.id}/1/delete")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Plot deleted successfully", response.data)

