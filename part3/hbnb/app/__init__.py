from flask import Flask, redirect
from app.api.v1 import api_bp
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
    
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    """Create app Flask """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure JWT
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
    
    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Configure JWT callbacks
    from app.api import configure_jwt
    configure_jwt(jwt)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Root route redirects to Swagger UI
    @app.route('/')
    def root():
        """Redirect to Swagger UI."""
        return redirect('/api/v1/doc/')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        """Return the health status of the application."""
        return {'status': 'healthy'}, 200
    
    return app