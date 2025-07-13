from flask import Flask, redirect
from app.api.v1 import api_bp
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    """
    Create and configure the Flask application.
    :param config_class: Configuration class
    :return: Configured Flask app
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # JWT settings
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600

    # Init extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # JWT callbacks
    from app.api import configure_jwt
    configure_jwt(jwt)

    # Register API blueprint
    app.register_blueprint(api_bp)

    # Redirect root to Swagger UI
    @app.route('/')
    def root():
        """Redirect to Swagger UI."""
        return redirect('/api/v1/doc/')

    # Health check
    @app.route('/health')
    def health():
        """Return health status."""
        return {'status': 'healthy'}, 200

    return app