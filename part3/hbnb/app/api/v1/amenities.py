from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import uuid

from app.models import amenity

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

"""MODELS"""
amenity_model = api.model('AmenityCreate', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_response = api.model('AmenityResponse', {
    'id': fields.String(description='Unique identifier for the amenity'),
    'name': fields.String(description='Name of the amenity')
})

"""ENDPOINTS"""
@api.route('/')
class AmenityList(Resource):
    @api.doc('create_amenity')
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_response, code=201)
    @api.response(400, 'Données invalides')
    @api.response(403, 'Administrateur requis')
    @api.response(409, 'Nom déjà utilisé')
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Administrateur requis'}, 403

        data = api.payload
        name = data['name'].strip()

        # Validation du nom
        if not name:
            return {'error': 'Le nom est requis'}, 400
        
        if not isinstance(name, str):
            return {'error': 'Le nom doit être une chaîne de caractères'}, 400

        # Vérifier si le nom existe déjà
        existing_amenity = facade.get_amenity_by_name(name)
        if existing_amenity:
            return {'error': 'Nom déjà utilisé'}, 409

        try:
            amenity_id = str(uuid.uuid4())
            amenity_data = {'id': amenity_id, 'name': name}
            amenity = facade.create_amenity(amenity_data)
            if not amenity:
                return {'error': 'Échec de la création de l\'équipement'}, 500
            
            return amenity.to_dict(), 201

        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500

    @api.doc('get_all_amenities')
    @api.marshal_list_with(amenity_response)
    def get(self):
        """Retrieve all amenities (public access)"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_response)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Retrieve a specific amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200
        
    @api.doc('update_amenity')
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_response)
    @api.response(404, 'Équipement non trouvé')
    @api.response(400, 'Données invalides')
    @api.response(403, 'Administrateur requis')
    @api.response(409, 'Nom déjà utilisé')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Administrateur requis'}, 403

        data = api.payload
        name = data['name'].strip()

        # Validation du nom
        if not name:
            return {'error': 'Le nom est requis'}, 400
        
        if not isinstance(name, str):
            return {'error': 'Le nom doit être une chaîne de caractères'}, 400

        try:
            # Vérifier si le nom existe déjà (en excluant l'équipement actuel)
            existing_amenity = facade.get_amenity_by_name(name)
            if existing_amenity and str(existing_amenity.id) != amenity_id:
                return {'error': 'Nom déjà utilisé'}, 409

            updated = facade.update_amenity(amenity_id, {'name': name})
            if not updated:
                return {'error': 'Équipement non trouvé'}, 404
            
            return updated.to_dict(), 200

        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500

    @api.doc('delete_amenity')
    @api.response(204, 'Équipement supprimé')
    @api.response(404, 'Équipement non trouvé')
    @api.response(403, 'Administrateur requis')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity by ID"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Administrateur requis'}, 403

        try:
            success = facade.delete_amenity(amenity_id)
            if not success:
                return {'error': 'Équipement non trouvé'}, 404
            return '', 204
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500

