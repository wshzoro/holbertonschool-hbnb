import unittest
import json
from app import create_app, bcrypt
from app.models.user import User
from app.services.facade import HBnBFacade

class TestAuth(unittest.TestCase):
    def setUp(self):
        """Set up test client and sample data."""
        self.app = create_app('config.DevelopmentConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create a test user
        self.test_email = 'test@example.com'
        self.test_password = 'testpass123'
        self.test_user = User(
            first_name='Test',
            last_name='User',
            email=self.test_email,
            password=self.test_password
        )
        
        # Add test user to the repository
        self.facade = HBnBFacade()
        self.facade.user_repo.add(self.test_user)
    
    def tearDown(self):
        """Clean up after tests."""
        self.app_context.pop()
    
    def test_successful_login(self):
        """Test successful user login with correct credentials."""
        response = self.client.post('/api/v1/auth/login', 
                                 data=json.dumps({
                                     'email': self.test_email,
                                     'password': self.test_password
                                 }),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.assertIn('user', data)
        self.assertEqual(data['user']['email'], self.test_email)
    
    def test_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post('/api/v1/auth/login', 
                                 data=json.dumps({
                                     'email': self.test_email,
                                     'password': 'wrongpassword'
                                 }),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_protected_route(self):
        """Test accessing a protected route with a valid token."""
        # First login to get a token
        login_response = self.client.post('/api/v1/auth/login', 
                                       data=json.dumps({
                                           'email': self.test_email,
                                           'password': self.test_password
                                       }),
                                       content_type='application/json')
        
        token = json.loads(login_response.data)['access_token']
        
        # Access protected route with token
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = self.client.get('/api/v1/protected/me', headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['email'], self.test_email)

if __name__ == '__main__':
    unittest.main()
