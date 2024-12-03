from tests.test_base import BaseTestCase
import json

class TestPiCalculation(BaseTestCase):
    def test_valid_calculation(self):
        """Test valid pi calculation request"""
        data = {
            **self.valid_credentials,
            'simulations': 1000,
            'concurrency': 2
        }
        response = self.client.post(
            '/pi',
            data=json.dumps(data),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIn('pi', result)
        self.assertIn('execution_time', result)
        
    def test_invalid_simulations(self):
        """Test invalid simulation count"""
        data = {
            **self.valid_credentials,
            'simulations': 50,  # Too low
            'concurrency': 2
        }
        response = self.client.post(
            '/pi',
            data=json.dumps(data),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 400)
        
    def test_async_calculation(self):
        """Test async pi calculation"""
        data = {
            **self.valid_credentials,
            'simulations': 1000,
            'concurrency': 2,
            'async': True
        }
        response = self.client.post(
            '/pi',
            data=json.dumps(data),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIn('task_id', result)
        self.assertIn('status', result)
        
    def test_high_concurrency(self):
        """Test maximum concurrency limit"""
        data = {
            **self.valid_credentials,
            'simulations': 1000,
            'concurrency': 65  # Above limit
        }
        response = self.client.post(
            '/pi',
            data=json.dumps(data),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 400)
        
    def test_high_simulations(self):
        """Test maximum simulations limit"""
        data = {
            **self.valid_credentials,
            'simulations': 100_000_001,  # Above limit
            'concurrency': 2
        }
        response = self.client.post(
            '/pi',
            data=json.dumps(data),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 400)
        
    def test_missing_parameters(self):
        """Test missing parameters"""
        data = {
            **self.valid_credentials
            # Missing simulations and concurrency
        }
        response = self.client.post(
            '/pi',
            data=json.dumps(data),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)  # Should use defaults 