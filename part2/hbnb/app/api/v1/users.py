from flask_restx import Namespace, Resource, fields
from app.services import facade
import re

api = Namespace('users')

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'place_list': fields.List(fields.String, required=True)
})

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data or email already registered')
    def post(self):
        """Create a new user"""
        data = api.payload

        if not data['first_name'].strip() or not data['last_name'].strip():
            return {'error': 'First name and last name are required'}, 400

        if not is_valid_email(data['email']):
            return {'error': 'Invalid email format'}, 400

        if len(data['password']) < 6:
            return {'error': 'Password must be at least 6 characters'}, 400

        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400

        user = facade.create_user(data)

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'place_list': user.place_list
        }, 201

    @api.response(200, 'Users retrieved')
    @api.response(404, 'No users found')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        if not users:
            return {'error': 'No users found'}, 404

        return [{
            'id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'place_list': u.place_list
        } for u in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User retrieved')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'place_list': user.place_list
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated')
    @api.response(400, 'Invalid data')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information"""
        data = api.payload

        if not data['first_name'].strip() or not data['last_name'].strip():
            return {'error': 'First name and last name are required'}, 400

        if not is_valid_email(data['email']):
            return {'error': 'Invalid email format'}, 400

        if len(data['password']) < 6:
            return {'error': 'Password must be at least 6 characters'}, 400

        user = facade.update_user(user_id, data)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'place_list': user.place_list
        }, 200
