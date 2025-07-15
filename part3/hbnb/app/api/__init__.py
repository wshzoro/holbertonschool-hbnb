from flask_restx import Api
from flask import Blueprint, redirect
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from flask_jwt_extended import JWTManager
from app.services.facade import HBnBFacade
facade = HBnBFacade()

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


def configure_jwt(jwt_manager: JWTManager):
    """Configure JWT callbacks."""
    @jwt_manager.user_identity_loader
    def user_identity_lookup(user):
        if isinstance(user, str):
            return user
        if isinstance(user, dict):
            return user['id']
        return str(user.id)

    @jwt_manager.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return facade.get_user(identity)

    @jwt_manager.additional_claims_loader
    def add_claims_to_access_token(identity):
        try:
            user_id = int(identity)  # Convertir l'identité en entier
            user = facade.get_user(user_id)
            return {'is_admin': user.is_admin if user else False}
        except (ValueError, TypeError):
            return {'is_admin': False}

