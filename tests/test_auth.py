import unittest
from app import create_app
from config import Config
from tests.test_base import BaseTestCase
import json

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Config)
        self.client = self.app.test_client()
        
    def test_valid_credentials(self):
        response = self.client.post('/test-auth', json={
            'username': '1234',
            'password': '1234-pw'
        })
        self.assertEqual(response.status_code, 200)
        
    def test_invalid_username(self):
        response = self.client.post('/test-auth', json={
            'username': '123',  # Only 3 digits
            'password': '123-pw'
        })
        self.assertEqual(response.status_code, 401)
        
    def test_invalid_password(self):
        response = self.client.post('/test-auth', json={
            'username': '1234',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 401)

class TestAuthentication(BaseTestCase):
    def test_valid_auth(self):
        """Test valid authentication"""
        response = self.client.post(
            '/auth',
            data=json.dumps(self.valid_credentials),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        
    def test_invalid_username(self):
        """Test invalid username format"""
        data = {
            'username': '123',  # Too short
            'password': '123-pw'
        }
        response = self.client.post(
            '/auth',
            data=json.dumps(data),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 401)
        
    def test_invalid_password(self):
        """Test invalid password format"""
        data = {
            'username': '1234',
            'password': 'wrong-password'
        }
        response = self.client.post(
            '/auth',
            data=json.dumps(data),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 401)
        
    def test_missing_credentials(self):
        """Test missing credentials"""
        response = self.client.post(
            '/auth',
            data=json.dumps({}),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 