from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if not claims.get('is_admin'):
                return {'error': 'Administrateur requis'}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
