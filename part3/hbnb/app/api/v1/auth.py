from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from app import bcrypt
import traceback
from datetime import timedelta

auth_ns = Namespace('auth', description='Authentication operations')

# Exposer le namespace
api = auth_ns

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Model for admin token response
admin_token_model = api.model('AdminTokenResponse', {
    'access_token': fields.String(description='JWT token'),
    'user': fields.Nested(api.model('AdminUser', {
        'id': fields.String(description='User ID'),
        'email': fields.String(description='User email'),
        'first_name': fields.String(description='User first name'),
        'last_name': fields.String(description='User last name'),
        'is_admin': fields.Boolean(description='Is admin')
    }))
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user:
            return {'error': 'Invalid credentials'}, 401
        
        # Vérifier le mot de passe avec bcrypt
        if not bcrypt.check_password_hash(user.password_hash, credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
        
        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200

@api.route('/admin-token')
class AdminToken(Resource):
    @api.doc(description='Get an admin token for development purposes')
    @api.response(200, 'Success', admin_token_model)
    @api.response(500, 'Failed to generate admin token')
    def get(self):
        """Get an admin token for development purposes"""
        try:
            admin = facade.get_user_by_email('admin@hbnb.com')
            if not admin:
                # Créer l'administrateur par défaut
                admin_data = {
                    'email': 'admin@hbnb.com',
                    'first_name': 'Admin',
                    'last_name': 'System',
                    'password': 'hbnb_admin_123!',
                    'is_admin': True
                }
                admin = facade.create_user(admin_data)
                if not admin:
                    raise ValueError("Failed to create admin user")
            
            access_token = create_access_token(
                identity={'id': str(admin.id), 'is_admin': True},
                expires_delta=timedelta(days=1)
            )
            
            return {
                'access_token': access_token,
                'user': {
                    'id': admin.id,
                    'email': admin.email,
                    'first_name': admin.first_name,
                    'last_name': admin.last_name,
                    'is_admin': admin.is_admin
                }
            }, 200
        except Exception as e:
            traceback.print_exc()
            return {
                'error': 'Failed to generate admin token',
                'details': str(e)
            }, 500