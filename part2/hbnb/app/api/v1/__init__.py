from flask_restx import Api
from flask import Blueprint

# Création du blueprint principal
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, title='HBnB API', version='1.0', description='A simple HBnB clone API')

# Import des namespaces
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.users import api as users_ns

# Enregistrement du namespace
api.add_namespace(reviews_ns, path='/reviews')
api.add_namespace(users_ns, path='/users')

