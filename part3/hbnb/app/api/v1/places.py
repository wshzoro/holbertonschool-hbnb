from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

""" Models """
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String,
    'name': fields.String
})

user_model = api.model('PlaceUser', {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String
})

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String, required=False),
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        data = api.payload
        data['owner_id'] = current_user_id

        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except PermissionError:
            return {'error': 'Unauthorized'}, 401

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        try:
            place = facade.get_place(place_id)
            return place.to_dict(include_owner=True, include_amenities=True), 200
        except ValueError:
            return {'error': 'Place not found'}, 404

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()

    def put(self, place_id):
        current_user_id = get_jwt_identity()
        data = api.payload

        try:
            place = facade.get_place(place_id)
            if place.owner_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            updated_place = facade.update_place(place_id, data)
            return {"message": "Place updated successfully"}, 200
        
        except ValueError as e:
            return {'error': str(e)}, 404
