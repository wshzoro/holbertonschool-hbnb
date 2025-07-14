from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('reviews', description='Reviews related operations')
facade = HBnBFacade()

""" Models """
review_create = api.model('ReviewCreate', {
    'text': fields.String(required=True, description='The content of the review'),
    'rating': fields.Integer(required=True, description='Rating between 1 and 5'),
    'user_id': fields.String(required=True, description='User ID who posted the review'),
    'place_id': fields.String(required=True, description='Place ID being reviewed')
})

review_response = api.model('ReviewResponse', {
    'id': fields.String(description='The unique identifier of the review'),
    'text': fields.String(description='The content of the review'),
    'rating': fields.Integer(description='Rating between 1 and 5'),
    'user_id': fields.String(description='User ID who posted the review'),
    'place_id': fields.String(description='Place ID being reviewed')
})

""" Endpoints """
@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.marshal_list_with(review_response)
    def get(self):
        """List all reviews"""
        return facade.get_all_reviews()

    @api.doc('create_review')
    @api.expect(review_create, validate=True)
    @api.marshal_with(review_response, code=201)
    @jwt_required()
    def post(self):
        """Create a new review"""   
        current_user_id = get_jwt_identity()
        data = api.payload
        data['user_id'] = current_user_id

        # Vérifier que l'utilisateur est authentifié
        if not current_user_id:
            return {'error': 'Authentication required'}, 401

        try:
            # Vérifier l'existence du lieu
            place = facade.get_place(data['place_id'])
            if not place:
                return {'error': 'Lieu non trouvé'}, 404

            # Vérifier que l'utilisateur n'est pas propriétaire du lieu
            if place.owner_id == current_user_id:
                return {'error': 'Vous ne pouvez pas évaluer votre propre lieu'}, 400

            # Vérifier si l'utilisateur a déjà créé un avis pour ce lieu
            existing_review = facade.get_review_by_user_and_place(current_user_id, data['place_id'])
            if existing_review:
                return {'error': 'Vous avez déjà évalué ce lieu'}, 400

            # Valider les données
            if not data.get('text') or not isinstance(data['text'], str):
                return {'error': 'Le texte est requis et doit être une chaîne de caractères'}, 400
            
            if not isinstance(data.get('rating'), int) or not (1 <= data['rating'] <= 5):
                return {'error': 'La note doit être un entier entre 1 et 5'}, 400

            # Créer l'avis
            review = facade.create_review(data)
            if not review:
                return {'error': 'Échec de la création de l\'avis'}, 500

            return  {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500

""" GET REVIEWS BY PLACE """
@api.route('/places/<place_id>')
class ReviewsByPlace(Resource):
    @api.doc('list_reviews_by_place')
    @api.marshal_list_with(review_response)
    def get(self, place_id):
        """List all reviews for a specific place"""
        return facade.get_reviews_by_place(place_id)

""" GET REVIEWS BY USER """
@api.route('/users/<user_id>')
class ReviewsByUser(Resource):
    @api.doc('list_reviews_by_user')
    @api.marshal_list_with(review_response)
    def get(self, user_id):
        """List all reviews by a specific user"""
        return facade.get_reviews_by_user(user_id)

# Endpoint pour gérer un review spécifique
@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')

class ReviewResource(Resource):
    @api.doc('get_review')
    @api.marshal_with(review_response)
    def get(self, review_id):
        """Retrieve a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Review {review_id} not found")
        return review

    """ UPDATE REVIEW """
    @api.doc('update_review')
    @api.expect(review_create, validate=True)
    @api.marshal_with(review_response)
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        data = api.payload

        try:
            # Récupérer l'avis
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Avis non trouvé'}, 404

            # Les administrateurs peuvent modifier tous les avis
            if not claims.get('is_admin') and review.user_id != current_user_id:
                return {'error': 'Action non autorisée'}, 403

            # Valider les données
            if 'text' in data and not isinstance(data['text'], str):
                return {'error': 'Le texte doit être une chaîne de caractères'}, 400
            
            if 'rating' in data and (not isinstance(data['rating'], int) or not (1 <= data['rating'] <= 5)):
                return {'error': 'La note doit être un entier entre 1 et 5'}, 400

            # Mettre à jour l'avis
            updated_review = facade.update_review(review_id, data)
            if not updated_review:
                return {'error': 'Échec de la mise à jour de l\'avis'}, 500

            return updated_review

        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500

    """ DELETE REVIEW """
    @api.doc('delete_review')
    @api.response(204, 'Avis supprimé')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review by ID""" 
        claims = get_jwt()
        current_user_id = get_jwt_identity()

        try:
            # Récupérer l'avis
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Avis non trouvé'}, 404

            # Les administrateurs peuvent supprimer tous les avis
            if not claims.get('is_admin') and review.user_id != current_user_id:
                return {'error': 'Action non autorisée'}, 403

            # Supprimer l'avis
            if facade.delete_review(review_id):
                return '', 204
            else:
                return {'error': 'Échec de la suppression de l\'avis'}, 500

        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
