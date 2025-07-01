from flask import Flask, redirect
from app.api.v1 import api_bp

def create_app():
    """Créer l'application Flask avec les routes de redirection et de santé."""
    app = Flask(__name__)
    app.config['DEBUG'] = True
    
    # Enregistrer le blueprint
    app.register_blueprint(api_bp)
    
    # Route racine qui redirige vers Swagger UI
    @app.route('/')
    def root():
        """Rediriger vers la documentation Swagger."""
        return redirect('/api/v1/doc/')
    
    # Route de santé
    @app.route('/health')
    def health():
        """Retourner l'état de santé de l'application."""
        return {'status': 'healthy'}, 200
    
    return app