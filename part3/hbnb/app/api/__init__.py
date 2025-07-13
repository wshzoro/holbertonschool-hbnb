from flask_restx import Api
from flask import Blueprint, redirect
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from .auth import api as auth_ns

# Import blueprint from v1
from app.api.v1 import api_bp, api as api_v1

# Add root route that redirects to Swagger UI
@api_bp.route('/')
def api_root():
    """Redirect to Swagger UI."""
    return redirect('/api/v1/doc/')

# Add namespaces
api_v1.add_namespace(amenities_ns, path='/amenities')
api_v1.add_namespace(users_ns, path='/users')
api_v1.add_namespace(places_ns, path='/places')
api_v1.add_namespace(reviews_ns, path='/reviews')
api_v1.add_namespace(auth_ns, path='/auth')

