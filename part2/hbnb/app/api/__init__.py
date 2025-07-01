from flask_restx import Api
from flask import Blueprint, redirect
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

# Importer le blueprint depuis v1
from app.api.v1 import api_bp, api as api_v1

# Ajouter une route racine qui redirige vers Swagger UI
@api_bp.route('/')
def api_root():
    """Rediriger vers la documentation Swagger."""
    return redirect('/api/v1/doc/')

# Ajouter les namespaces
api_v1.add_namespace(amenities_ns, path='/amenities')
api_v1.add_namespace(users_ns, path='/users')
api_v1.add_namespace(places_ns, path='/places')
api_v1.add_namespace(reviews_ns, path='/reviews')
# api.add_namespace(places_ns)
# api.add_namespace(reviews_ns)