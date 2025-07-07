from flask_restx import Api
from flask import Blueprint

# Création du blueprint principal
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp, title='HBnB API', version='1.0', description='A simple HBnB clone API', doc='/doc/')

# Import des namespaces
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

# Enregistrement des namespaces
api.add_namespace(amenities_ns, path='/amenities')
api.add_namespace(users_ns, path='/users')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')

# Exposer le Blueprint et l'API
__all__ = ['api_bp', 'api']
