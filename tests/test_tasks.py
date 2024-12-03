from tests.test_base import BaseTestCase
import json
import time

class TestTaskManagement(BaseTestCase):
    def test_task_lifecycle(self):
        """Test complete task lifecycle"""
        # Create task
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
        task_id = result['task_id']
        
        # Wait for task completion
        time.sleep(2)
        
        # Check task status
        response = self.client.get(
            f'/task/{task_id}',
            headers=self.auth_headers,
            data=json.dumps(self.valid_credentials)
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIn('status', result) 

    def test_invalid_task_id(self):
        """Test invalid task ID"""
        response = self.client.get(
            '/task/invalid-id',
            headers=self.auth_headers,
            data=json.dumps(self.valid_credentials)
        )
        self.assertEqual(response.status_code, 404)
        
    def test_task_cleanup(self):
        """Test task cleanup"""
        # Create a task
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
        
        # Trigger cleanup
        cleanup_data = {
            **self.valid_credentials,
            'max_age': 0  # Immediate cleanup
        }
        response = self.client.post(
            '/task/cleanup',
            headers=self.auth_headers,
            data=json.dumps(cleanup_data)
        )
        self.assertEqual(response.status_code, 200) 