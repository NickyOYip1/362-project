import unittest
from app import create_app
from config import TestConfig

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.auth_headers = {
            'Content-Type': 'application/json'
        }
        self.valid_credentials = {
            'username': '1234',
            'password': '1234-pw'
        } 