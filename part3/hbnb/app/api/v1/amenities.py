from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid

from part3.hbnb.app.models import amenity

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
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        data = api.payload
        name = data['name'].strip()
        if not name:
            return {'error': 'Missing or invalid amenity name'}, 400
        try:
            amenity_id = str(uuid.uuid4())
            amenity_data = {'id': amenity_id, 'name': name}
            amenity = facade.create_amenity(amenity_data)
            return amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

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
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = api.payload
        name = data['name'].strip()
        if not name:
            return {'error': 'Missing or invalid amenity name'}, 400
        try:
            updated = facade.update_amenity(amenity_id, {'name': name})
            if not updated:
                return {'error': 'Amenity not found'}, 404
            return updated.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.doc('delete_amenity')
    @api.response(204, 'Amenity deleted')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity by ID"""
        success = facade.delete_amenity(amenity_id)
        if not success:
            return {'error': 'Amenity not found'}, 404
        return '', 204

