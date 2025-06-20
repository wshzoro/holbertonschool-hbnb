from flask_restx import Api
from flask import Blueprint
from app.api.v1.amenities import api as amenities_ns

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, title='HBnB API', version='1.0', description='HBnB REST API')

api.add_namespace(amenities_ns)
# api.add_namespace(users_ns)
# api.add_namespace(places_ns)
# api.add_namespace(reviews_ns)