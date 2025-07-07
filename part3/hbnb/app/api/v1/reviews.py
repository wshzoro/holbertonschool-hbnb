from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Reviews related operations')
facade = HBnBFacade()

# Modèle pour la création d'un review
review_model = api.model('ReviewCreate', {
    'text': fields.String(required=True, description='The content of the review'),
    'rating': fields.Integer(required=True, description='Rating between 1 and 5'),
    'user_id': fields.String(required=True, description='User ID who posted the review'),
    'place_id': fields.String(required=True, description='Place ID being reviewed')
})

# Modèle pour la réponse
review_response = api.model('ReviewResponse', {
    'id': fields.String(description='The unique identifier of the review'),
    'text': fields.String(description='The content of the review'),
    'rating': fields.Integer(description='Rating between 1 and 5'),
    'user_id': fields.String(description='User ID who posted the review'),
    'place_id': fields.String(description='Place ID being reviewed')
})

# Endpoint pour lister et créer des reviews
@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.marshal_list_with(review_response)
    def get(self):
        """List all reviews"""
        return facade.get_all_reviews()

    @api.doc('create_review')
    @api.expect(review_model)
    @api.marshal_with(review_response, code=201)
    def post(self):
        """Create a new review"""
        data = api.payload
        try:
            # Valider les données
            if not isinstance(data['text'], str) or data['rating'] < 1 or data['rating'] > 5:
                return {'error': 'Rating must be an integer between 1 and 5'}, 400
                
            # Créer le review
            review = facade.create_review(data)
            return  {
                'id' : review.id,
                'text' : review.text,
                'rating' : review.rating,
                'user_id' : review.user_id,
                'place_id' : review.place_id
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400

# Endpoint pour récupérer les reviews d'un lieu spécifique
@api.route('/places/<place_id>')
class ReviewsByPlace(Resource):
    @api.doc('list_reviews_by_place')
    @api.marshal_list_with(review_response)
    def get(self, place_id):
        """List all reviews for a specific place"""
        return facade.get_reviews_by_place(place_id)

# Endpoint pour récupérer les reviews d'un utilisateur spécifique
@api.route('/users/<user_id>')
class ReviewsByUser(Resource):
    @api.doc('list_reviews_by_user')
    @api.marshal_list_with(review_response)
    def get(self, user_id):
        """List all reviews by a specific user"""
        return facade.get_reviews_by_user(user_id)

# Endpoint pour gérer un review spécifique
@api.route('/<string:review_id>')
@api.response(404, 'Review not found')
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

    @api.doc('delete_review')
    @api.response(204, 'Review deleted')
    def delete(self, review_id):
        """Delete a review by ID"""
        if not facade.delete_review(review_id):
            api.abort(404, f"Review {review_id} not found")
        return '', 204
    def get(self, review_id):
        """Fetch a review given its identifier"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review

    @api.doc('update_review')
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update a review given its identifier"""
        review = facade.update_review(review_id, request.json)
        if not review:
            api.abort(404, "Review not found")
        return review

    @api.doc('delete_review')
    @api.response(204, 'Review deleted')
    def delete(self, review_id):
        """Delete a review given its identifier"""
        success = facade.delete_review(review_id)
        if not success:
            api.abort(404, "Review not found")
        return '', 204