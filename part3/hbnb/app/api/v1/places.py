from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

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
        """Create a new place"""
        current_user_id = get_jwt_identity()
        data = api.payload
        
        # Vérifier que l'utilisateur est bien propriétaire du lieu
        if data.get('owner_id') and data['owner_id'] != current_user_id:
            return {'error': 'Cannot create place for another user'}, 403
            
        # Forcer l'owner_id à être l'ID de l'utilisateur actuel
        data['owner_id'] = current_user_id

        try:
            # Valider les données avant la création
            if not data.get('title') or not isinstance(data['title'], str):
                return {'error': 'Title is required and must be a string'}, 400
            if not isinstance(data.get('price'), (int, float)) or data['price'] <= 0:
                return {'error': 'Price must be a positive number'}, 400
            if not isinstance(data.get('latitude'), (int, float)) or not isinstance(data.get('longitude'), (int, float)):
                return {'error': 'Latitude and longitude must be numbers'}, 400

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
    @api.response(200, 'Lieu mis à jour')
    @api.response(404, 'Lieu non trouvé')
    @api.response(400, 'Données invalides')
    @api.response(403, 'Action non autorisée')
    @jwt_required()
    def put(self, place_id):
        """Update a place"""
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        data = api.payload

        try:
            # Récupérer le lieu
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Lieu non trouvé'}, 404

            # Les administrateurs peuvent modifier tous les lieux
            if not claims.get('is_admin') and place.owner_id != current_user_id:
                return {'error': 'Action non autorisée'}, 403

            # Valider les données
            if data.get('title') and not isinstance(data['title'], str):
                return {'error': 'Le titre doit être une chaîne de caractères'}, 400
            if data.get('price') and (not isinstance(data['price'], (int, float)) or data['price'] <= 0):
                return {'error': 'Le prix doit être un nombre positif'}, 400
            if (data.get('latitude') and not isinstance(data['latitude'], (int, float))) or \
               (data.get('longitude') and not isinstance(data['longitude'], (int, float))):
                return {'error': 'La latitude et la longitude doivent être des nombres'}, 400

            # Mettre à jour le lieu
            updated_place = facade.update_place(place_id, data)
            if not updated_place:
                return {'error': 'Échec de la mise à jour du lieu'}, 500

            return updated_place.to_dict(), 200

        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
            if not place:
                return {'error': 'Place not found'}, 404
            
            # Vérifier que l'utilisateur est le propriétaire
            if place.owner_id != current_user_id:
                return {'error': 'Action non autorisée'}, 403

            # Valider les données avant la mise à jour
            if 'title' in data and not isinstance(data['title'], str):
                return {'error': 'Title must be a string'}, 400
            if 'price' in data and (not isinstance(data['price'], (int, float)) or data['price'] <= 0):
                return {'error': 'Price must be a positive number'}, 400
            if 'latitude' in data and not isinstance(data['latitude'], (int, float)):
                return {'error': 'Latitude must be a number'}, 400
            if 'longitude' in data and not isinstance(data['longitude'], (int, float)):
                return {'error': 'Longitude must be a number'}, 400

            # Mettre à jour le lieu
            updated_place = facade.update_place(place_id, data)
            if not updated_place:
                return {'error': 'Failed to update place'}, 500

            return {"message": "Place updated successfully"}, 200
        
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error'}, 500
