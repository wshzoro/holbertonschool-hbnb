from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
import re
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

facade = HBnBFacade()

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'place_list': fields.List(fields.String, required=False)
})

# Modèle pour la création d'utilisateur avec mot de passe
user_create_model = api.clone('UserCreate', user_model, {
    'password': fields.String(required=True)
})

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@api.route('/')
class UserList(Resource):
    @api.expect(user_create_model, validate=True)
    @api.response(201, 'Utilisateur créé')
    @api.response(400, 'Données invalides')
    @api.response(403, 'Administrateur requis')
    @api.response(409, 'Email déjà enregistré')
    @jwt_required()
    def post(self):
        """Create a new user"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Administrateur requis'}, 403

        data = api.payload

        # Validation des données
        if not data.get('first_name') or not data.get('last_name'):
            return {'error': 'Le prénom et le nom sont requis'}, 400
        
        if not isinstance(data.get('first_name'), str) or not isinstance(data.get('last_name'), str):
            return {'error': 'Le prénom et le nom doivent être des chaînes de caractères'}, 400

        if not data.get('email') or not is_valid_email(data['email']):
            return {'error': 'Format d\'email invalide'}, 400

        if not data.get('password') or len(data['password']) < 6:
            return {'error': 'Le mot de passe doit contenir au moins 6 caractères'}, 400

        # Vérification de l'unicité de l'email
        if facade.get_user_by_email(data['email']):
            return {'error': 'Email déjà enregistré'}, 409

        # Création de l'utilisateur
        try:
            user = facade.create_user(data)
            if not user:
                return {'error': 'Échec de la création de l\'utilisateur'}, 500

            return {
                'id': str(user.id),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'message': 'Utilisateur créé'
            }, 201

        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500

    @api.response(200, 'Users retrieved')
    @api.response(404, 'No users found')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        #if not users:
         #   return {'error': 'No users found'}, 404

        return [{
            'id': u.id,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'place_list': u.place_list
        } for u in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'Utilisateur récupéré')
    @api.response(404, 'Utilisateur non trouvé')
    @jwt_required()
    def get(self, user_id):
        """Retrieve a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'Utilisateur non trouvé'}, 404
            
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

    @api.expect(user_model)
    @api.response(200, 'Utilisateur mis à jour')
    @api.response(400, 'Données invalides')
    @api.response(403, 'Action non autorisée')
    @api.response(404, 'Utilisateur non trouvé')
    @api.response(409, 'Email déjà enregistré')
    @jwt_required()
    def put(self, user_id):
        """Update user information"""
        claims = get_jwt()
        current_user_id = get_jwt_identity()

        try:
            # Les administrateurs peuvent modifier tous les utilisateurs
            if not claims.get('is_admin') and current_user_id != user_id:
                return {'error': 'Action non autorisée'}, 403

            data = api.payload
            
            # Valider les données
            if not data.get('first_name') or not data.get('last_name'):
                return {'error': 'Le prénom et le nom sont requis'}, 400
            
            if not isinstance(data.get('first_name'), str) or not isinstance(data.get('last_name'), str):
                return {'error': 'Le prénom et le nom doivent être des chaînes de caractères'}, 400

            # Vérifier l'unicité de l'email si il est fourni
            if data.get('email'):
                existing_user = facade.get_user_by_email(data['email'])
                if existing_user and str(existing_user.id) != user_id:
                    return {'error': 'Email déjà enregistré'}, 409

            # Mettre à jour l'utilisateur
            user = facade.update_user(user_id, data)
            if not user:
                return {'error': 'Utilisateur non trouvé'}, 404

            return {
                'id': str(user.id),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'place_list': user.place_list
            }, 200

        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
