from flask import Flask, redirect
from app.api.v1 import api_bp

def create_app(config_class="config.DevelopmentConfig"):
    """Create app Flask """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Save blueprint
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