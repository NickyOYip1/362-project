import requests
import time

def test_auth():
    url = 'http://localhost:5000/test-auth'
    
    # Test valid credentials
    print("\nTesting valid credentials:")
    valid_data = {
        'username': '1234',
        'password': '1234-pw'
    }
    response = requests.post(url, json=valid_data)
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Raw Response: {response.text}")
    
    # Test invalid credentials
    print("\nTesting invalid credentials:")
    invalid_data = {
        'username': '123',
        'password': 'wrong'
    }
    response = requests.post(url, json=invalid_data)
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Raw Response: {response.text}")

def test_pi():
    url = 'http://localhost:5000/pi'
    
    # Test valid pi calculation
    print("\nTesting valid pi calculation:")
    valid_data = {
        'username': '1234',
        'password': '1234-pw',
        'simulations': 1000,
        'concurrency': 2
    }
    response = requests.post(url, json=valid_data)
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Raw Response: {response.text}")
    
    # Test invalid pi calculation
    print("\nTesting invalid pi calculation:")
    invalid_data = {
        'username': '1234',
        'password': '1234-pw',
        'simulations': 50,  # Too low
        'concurrency': 2
    }
    response = requests.post(url, json=invalid_data)
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Raw Response: {response.text}")

def test_legacy_pi():
    url = 'http://localhost:5000/legacy_pi'
    
    # Test TCP request
    print("\nTesting TCP legacy pi calculation:")
    tcp_data = {
        'username': '1234',
        'password': '1234-pw',
        'protocol': 'tcp'
    }
    response = requests.post(url, json=tcp_data)
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Raw Response: {response.text}")
    
    # Test UDP request
    print("\nTesting UDP legacy pi calculation:")
    udp_data = {
        'username': '1234',
        'password': '1234-pw',
        'protocol': 'udp'
    }
    response = requests.post(url, json=udp_data)
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Raw Response: {response.text}")

def test_statistics():
    url = 'http://localhost:5000/statistics'
    headers = {
        'Content-Type': 'application/json'
    }
    auth_data = {
        'username': '1234',
        'password': '1234-pw'
    }
    
    # Test get statistics
    print("\nTesting get statistics:")
    response = requests.get(
        url, 
        json=auth_data,
        headers=headers
    )
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Raw Response: {response.text}")
    
    # Test clear statistics
    print("\nTesting clear statistics:")
    response = requests.delete(
        url, 
        json=auth_data,
        headers=headers
    )
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Raw Response: {response.text}")

def test_task_management():
    print("\nTesting Task Management:")
    
    # Test task creation
    print("\nTesting task creation:")
    url = 'http://localhost:5000/pi'
    headers = {'Content-Type': 'application/json'}
    data = {
        'username': '1234',
        'password': '1234-pw',
        'simulations': 1000,
        'concurrency': 2,
        'async': True
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
        task_id = response.json().get('task_id')
        
        if task_id:
            # Wait for task to complete
            print("\nWaiting for task to complete...")
            time.sleep(2)  # Give the task 2 seconds to complete
            
            # Test task status retrieval
            print("\nTesting task status:")
            status_url = f'http://localhost:5000/task/{task_id}'
            response = requests.get(
                status_url,
                headers=headers,
                json={'username': '1234', 'password': '1234-pw'}
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
            # If task is still pending, wait and try again
            if response.status_code == 200 and response.json().get('status') == 'pending':
                print("\nTask still pending, waiting longer...")
                time.sleep(3)  # Wait additional 3 seconds
                response = requests.get(
                    status_url,
                    headers=headers,
                    json={'username': '1234', 'password': '1234-pw'}
                )
                print(f"Final Status Code: {response.status_code}")
                print(f"Final Response: {response.json()}")
    except:
        print(f"Raw Response: {response.text}")

if __name__ == "__main__":
    print("Testing Authentication:")
    test_auth()
    print("\nTesting Pi Calculation:")
    test_pi()
    print("\nTesting Legacy Pi Calculation:")
    test_legacy_pi()
    print("\nTesting Statistics:")
    test_statistics()
    print("\nTesting Task Management:")
    test_task_management() 