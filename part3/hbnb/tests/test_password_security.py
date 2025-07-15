import unittest
import json
import os
import sys
import subprocess
from time import sleep
import requests
from app import create_app, db, bcrypt
from app.models.user import User

class TestPasswordSecurity(unittest.TestCase):
    def setUp(self):
        """Set up test client and sample data."""
        # Configuration de l'application de test
        from config import config
        self.app = create_app(config['testing'])
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Créer un utilisateur admin pour les tests
        admin = User(
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            password='adminpass123',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        
        # Obtenir le token JWT pour l'admin
        response = self.client.post(
            '/api/v1/auth/login',
            json={
                'email': 'admin@example.com',
                'password': 'adminpass123'
            }
        )
        self.admin_token = response.json()['access_token']

    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        """Test if password is properly hashed."""
        # Test data
        test_password = "testpass123"
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password=test_password
        )

        # Vérifier que le mot de passe est correctement haché
        self.assertNotEqual(user.password_hash, test_password)
        self.assertTrue(bcrypt.check_password_hash(user.password_hash, test_password))
        
        # Vérifier que le mot de passe n'est pas stocké en clair
        with self.assertRaises(AttributeError):
            _ = user.password

    def test_create_user_endpoint(self):
        """Test POST /api/v1/users/ endpoint."""
        # Données de test
        test_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "securepassword123",
            "is_admin": False
        }

        # Faire une requête POST avec le token admin
        headers = {
            'Authorization': f'Bearer {self.admin_token}'
        }
        response = self.client.post(
            '/api/v1/users/',
            json=test_data,
            headers=headers
        )

        # Vérifier la réponse
        self.assertEqual(response.status_code, 201)
        data = response.get_json()  # Use get_json() instead of response.json
        
        # Vérifier que le mot de passe n'est pas retourné
        self.assertNotIn('password', data)
        self.assertNotIn('password_hash', data)
        
        # Vérifier que l'utilisateur a été créé avec succès
        self.assertIn('id', data)
        self.assertIn('email', data)
        self.assertEqual(data['email'], test_data['email'])
        
        # Vérifier que l'endpoint est protégé (requiert authentification)
        response_unauthorized = self.client.post(
            '/api/v1/users/',
            json=test_data
        )
        self.assertEqual(response_unauthorized.status_code, 401)

    def test_get_user_endpoint(self):
        """Test GET /api/v1/users/<user_id> endpoint."""
        # Créer un utilisateur pour les tests
        test_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "securepassword123",
            "is_admin": False
        }
        
        # Créer l'utilisateur avec le token admin
        headers = {
            'Authorization': f'Bearer {self.admin_token}'
        }
        response = self.client.post(
            '/api/v1/users/',
            json=test_data,
            headers=headers
        )
        user_id = response.json['id']

        # Tester la récupération de l'utilisateur
        response = self.client.get(
            f'/api/v1/users/{user_id}',
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn('email', data)
        self.assertNotIn('password', data)
        self.assertNotIn('password_hash', data)
        
        # Tester l'accès non autorisé
        response_unauthorized = self.client.get(
            f'/api/v1/users/{user_id}'
        )
        self.assertEqual(response_unauthorized.status_code, 401)

    def test_delete_user_endpoint(self):
        """Test DELETE /api/v1/users/<user_id> endpoint."""
        # Créer un utilisateur pour les tests
        test_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "securepassword123",
            "is_admin": False
        }
        
        # Créer l'utilisateur avec le token admin
        headers = {
            'Authorization': f'Bearer {self.admin_token}'
        }
        response = self.client.post(
            '/api/v1/users/',
            json=test_data,
            headers=headers
        )
        user_id = response.json['id']

        # Tester la suppression de l'utilisateur
        response = self.client.delete(
            f'/api/v1/users/{user_id}',
            headers=headers
        )
        self.assertEqual(response.status_code, 204)
        
        # Vérifier que l'utilisateur a été supprimé
        response = self.client.get(
            f'/api/v1/users/{user_id}',
            headers=headers
        )
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
