import unittest, datetime
from flask import current_app
from liquidnet import create_app, config, db
from liquidnet.library.models import User, BookRequests, Books
import json


class TestLibraryAPIs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_obj = create_app(configuration=config.TestConfig)

    def setUp(self):
        with self.app_obj.app_context():
            self.app = current_app.test_client()
            db.drop_all()
            db.create_all()

            book=Books(title="Test text book", author='Test author')
            db.session.add(book)
            db.session.commit()

    def tearDown(self):
        with self.app_obj.app_context():
            db.drop_all()

    def add_request(self, data):
        response = self.app.post('/request',
                                 data=json.dumps(data),
                                 content_type='application/json')
        return response

    def test_home(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_request_when_title_exists(self):
        # This book has been added to database in Setup and hence is a valid request.
        data = {"email": "test_eoin@company.com", "title": "Test text book"}
        response = self.app.post('/request', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'"title": "Test text book"', response.data)

    def test_create_request_when_title_does_not_exist(self):
        data = {"email": "test_eoin@company.com", "title": "Wrong book"}
        response = self.app.post('/request', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'The book with this title does not exist', response.data)

    def test_create_request_when_email_is_invalid(self):
        data = {"email": "test_eoin-company.com", "title": "Test text book"}
        response = self.app.post('/request', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Not a valid email address', response.data)

    def test_list_all_requests_when_requests_exist(self):
        self.add_request({"email": "testsean@company.com", "title": "Test text book"})
        self.add_request({"email": "ben@company.com", "title": "Test text book"})
        self.add_request({"email": "ron@company.com", "title": "Test text book"})

        response = self.app.get('/request')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"email": "testsean@company.com"', response.data)
        self.assertIn(b'"email": "ben@company.com"', response.data)
        self.assertIn(b'"email": "ron@company.com"', response.data)

    def test_get_a_request_that_exists(self):
        record = self.add_request({"email": "testsean@company.com", "title": "Test text book"})
        record_json = json.loads(record.data)
        record_id = record_json.get('id')
        response = self.app.get('/request/{}'.format(record_id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test text book', response.data)

    def test_get_a_request_that_does_not_exist(self):
        response = self.app.get('/request/{}'.format(5))
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Request by this ID is not found', response.data)

    def test_delete_request_by_valid_id(self):
        record = self.add_request({"email": "testsean@company.com", "title": "Test text book"})
        record_json = json.loads(record.data)
        record_id = record_json.get('id')
        response = self.app.delete('/request/{}'.format(record_id))
        self.assertEqual(response.status_code, 200)

    def test_delete_request_by_invalid_id(self):
        response = self.app.delete('/request/{}'.format(5))
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'"error": "Request by this ID is not found"', response.data)
