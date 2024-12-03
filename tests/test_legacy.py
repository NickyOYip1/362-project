from tests.test_base import BaseTestCase
import json

class TestLegacyService(BaseTestCase):
    def test_tcp_request(self):
        """Test TCP legacy request"""
        data = {
            **self.valid_credentials,
            'protocol': 'tcp'
        }
        response = self.client.post(
            '/legacy_pi',
            data=json.dumps(data),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIn('pi', result)
        self.assertIn('protocol', result)
        
    def test_udp_request(self):
        """Test UDP legacy request"""
        data = {
            **self.valid_credentials,
            'protocol': 'udp'
        }
        response = self.client.post(
            '/legacy_pi',
            data=json.dumps(data),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIn('pi', result)
        self.assertIn('protocol', result)
        
    def test_invalid_protocol(self):
        """Test invalid protocol"""
        data = {
            **self.valid_credentials,
            'protocol': 'invalid'
        }
        response = self.client.post(
            '/legacy_pi',
            data=json.dumps(data),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 400)
        
    def test_missing_protocol(self):
        """Test missing protocol"""
        data = {
            **self.valid_credentials
            # Missing protocol
        }
        response = self.client.post(
            '/legacy_pi',
            data=json.dumps(data),
            headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)  # Should use default (tcp)
  