from tests.test_base import BaseTestCase
import json

class TestStatistics(BaseTestCase):
    def test_get_statistics(self):
        """Test getting statistics"""
        response = self.client.get(
            '/statistics',
            headers=self.auth_headers,
            data=json.dumps(self.valid_credentials)
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIsInstance(result, list)
        
    def test_clear_statistics(self):
        """Test clearing statistics"""
        response = self.client.delete(
            '/statistics',
            headers=self.auth_headers,
            data=json.dumps(self.valid_credentials)
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIn('message', result) 