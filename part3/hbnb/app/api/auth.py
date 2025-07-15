from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import hbnb_facade as facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from datetime import datetime, timedelta

# Utilisateur administrateur par défaut
DEFAULT_ADMIN = {
    'id': '00000000-0000-0000-0000-000000000000',
    'email': 'admin@hbnb.com',
    'password': 'hbnb_admin_123!',  # À changer en production
    'first_name': 'Admin',
    'last_name': 'System',
    'is_admin': True
}

def get_or_create_default_admin():
    """Crée ou récupère l'utilisateur administrateur par défaut"""
    try:
        # Essayer de récupérer l'admin par email
        admin = facade.get_user_by_email(DEFAULT_ADMIN['email'])
        if not admin:
            print("[AUTH] Creating default admin user...")
            # Créer un nouvel utilisateur admin via le service utilisateur
            admin = facade.user_service.create_user(
                email=DEFAULT_ADMIN['email'],
                first_name=DEFAULT_ADMIN['first_name'],
                last_name=DEFAULT_ADMIN['last_name'],
                password=DEFAULT_ADMIN['password'],  # Le service va hasher le mot de passe
                is_admin=True
            )
            print(f"[AUTH] Created admin user: {admin.id}")
        return admin
    except Exception as e:
        print(f"[AUTH] Error in get_or_create_default_admin: {str(e)}")
        raise

auth_ns = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = auth_ns.payload  # Get the email and password from the request payload
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with just the user's id
        access_token = create_access_token(identity=str(user.id))
        
        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200

@auth_ns.route('/admin-token')
class AdminToken(Resource):
    @auth_ns.doc(description='Get an admin token for development purposes')
    @auth_ns.response(200, 'Success', auth_ns.model('AdminTokenResponse', {
        'access_token': fields.String(description='JWT token'),
        'user': fields.Nested(auth_ns.model('AdminUser', {
            'id': fields.String(description='User ID'),
            'email': fields.String(description='User email'),
            'first_name': fields.String(description='User first name'),
            'last_name': fields.String(description='User last name'),
            'is_admin': fields.Boolean(description='Is admin')
        }))
    }))
    @auth_ns.response(500, 'Failed to generate admin token')
    def get(self):
        """Get an admin token for development purposes"""
        try:
            admin = get_or_create_default_admin()
            access_token = create_access_token(
                identity=str(admin.id),
                expires_delta=timedelta(days=1)  # Token valable 24h
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
            print(f"[AUTH] Error generating admin token: {str(e)}")
            return {'error': 'Failed to generate admin token'}, 500

@auth_ns.route('/protected')
class Protected(Resource):
    @auth_ns.doc(description='Protected endpoint that requires a valid JWT token')
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {
            'message': f"Hello, user {current_user['id']}"
        }, 200
