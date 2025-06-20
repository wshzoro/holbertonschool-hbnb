from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Reviews related operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='The unique identifier of the review'),
    'text': fields.String(required=True, description='The content of the review'),
    'rating': fields.Integer(required=True, description='Rating between 1 and 5'),
    'user_id': fields.String(required=True, description='User ID who posted the review'),
    'place_id': fields.String(required=True, description='Place ID being reviewed')
})

@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.marshal_list_with(review_model)
    def get(self):
        """List all reviews"""
        return facade.get_all_reviews()

    @api.doc('create_review')
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        data = request.json
        try:
            return facade.create_review(data), 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:review_id>')
@api.response(404, 'Review not found')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.doc('get_review')
    @api.marshal_with(review_model)
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
