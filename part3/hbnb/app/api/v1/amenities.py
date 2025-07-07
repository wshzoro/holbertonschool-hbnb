from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
import uuid

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

# Modèle pour la création d'un amenity
amenity_model = api.model('AmenityCreate', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Modèle pour la réponse de création
create_response = api.model('CreateResponse', {
    'id': fields.String(description='Unique identifier for the amenity'),
    'name': fields.String(description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created', create_response)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        try:
            data = api.payload
            # Vérifier que le nom est présent
            if not data or 'name' not in data or not data['name'].strip():
                return {'error': 'Missing or invalid amenity name'}, 400
                
            # Générer un ID unique
            amenity_id = str(uuid.uuid4())
            amenity_data = {**data, 'id': amenity_id}
            amenity = facade.create_amenity(amenity_data)
            
            # Retourner la réponse avec le format attendu
            return amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Retrieve a specific amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            data = api.payload
            result = facade.update_amenity(amenity_id, data)
            if not result:
                return {"error": "Amenity not found"}, 404
            return result.to_dict(), 200
        except ValueError as ve:
            return {"error": str(ve)}, 400