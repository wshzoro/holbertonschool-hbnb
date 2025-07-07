from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import (
    create_access_token, 
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from app.services import facade

# Create namespaces
auth_ns = Namespace('auth', description='Authentication operations')
protected_ns = Namespace('protected', description='Protected routes')

# Request parsers
login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help='Email is required')
login_parser.add_argument('password', type=str, required=True, help='Password is required')

# Models
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

user_model = auth_ns.model('User', {
    'id': fields.String(description='User ID'),
    'email': fields.String(description='User email'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'is_admin': fields.Boolean(description='Is user admin')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Successfully logged in')
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """
        Authenticate user and return a JWT token
        """
        args = login_parser.parse_args()
        email = args.get('email')
        password = args.get('password')
        
        # Retrieve the user based on the provided email
        user = facade.get_user_by_email(email)
        
        # Check if the user exists and the password is correct
        if not user or not user.verify_password(password):
            return {'error': 'Invalid email or password'}, 401

        # Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
            identity={
                'id': str(user.id), 
                'is_admin': user.is_admin,
                'email': user.email
            }
        )
        
        # Return the JWT token to the client
        return {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': user.is_admin
            }
        }, 200

@protected_ns.route('/me')
class ProtectedResource(Resource):
    @jwt_required()
    @auth_ns.marshal_with(user_model)
    @auth_ns.response(200, 'Success')
    @auth_ns.response(401, 'Unauthorized')
    def get(self):
        """
        Get current user information
        Requires valid JWT token
        """
        current_user = get_jwt_identity()
        user = facade.get_user(current_user['id'])
        if not user:
            return {'error': 'User not found'}, 404
            
        return user, 200

@api.route('/')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        return {'message': f'Hello, user {user["id"]}'}
