from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.facade import HBnBFacade

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

""" CREATE"""
@api.doc('create_review')
@api.expect(review_create, validate=True)
@api.marshal_with(review_response, code=201)
@jwt_required()
def post(self):
    """Create a new review"""   
    current_user_id = get_jwt_identity()
    data = api.payload
    data['user_id'] = current_user_id

    if not (1 <= data['rating'] <= 5):
        return {'error': 'Rating must be an integer between 1 and 5'}, 400

    try:
        review = facade.create_review(data)
        return  {
                'id' : review.id,
                'text' : review.text,
                'rating' : review.rating,
                'user_id' : review.user_id,
                'place_id' : review.place_id
            }, 201
    except ValueError as e:
        return {'error': str(e)}, 400

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
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update a review given its identifier"""
        current_user_id = get_jwt_identity()
        review = facade.update_review(review_id, request.json)
        if not review:
            api.abort(404, "Review not found")

        """check authors"""
        if review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403    
        playload = request.json
        if 'rating' in playload and not (1 <= playload['rating'] <= 5):
            return {'error': 'Rating must be an integer between 1 and 5'}, 400
        try:
            updated_review = facade.update_review(review_id, playload)
            return updated_review
        except ValueError as e:
            return {'error': str(e)}, 400

"""DELETE REVIEW"""
@api.doc('delete_review')
@api.response(204, 'Review deleted')
@jwt_required()
def delete(self, review_id):
        """Delete a review by ID""" 
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Review {review_id} not found")
        if review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        if not facade.delete_review(review_id):
            api.abort(404, f"Review {review_id} not found")
        return '', 204
