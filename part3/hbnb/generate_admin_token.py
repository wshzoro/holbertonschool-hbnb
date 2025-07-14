from app import create_app
from app.models.user import User
from flask_jwt_extended import create_access_token, decode_token

def generate_admin_token():
    app = create_app()
    with app.app_context():
        # Récupérer l'utilisateur admin
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            print("Erreur: L'admin n'existe pas")
            return
        
        # Créer un nouveau token avec le rôle admin
        token = create_access_token(identity=str(admin.id))
        print("Token JWT pour l'admin:")
        print(token)
        
        # Vérifier le token
        try:
            claims = decode_token(token)
            print("\nClaims du token:")
            print(f"ID: {claims.get('sub')}")
            print(f"Is admin: {claims.get('is_admin')}")
        except Exception as e:
            print(f"Erreur lors de la vérification du token: {str(e)}")

if __name__ == '__main__':
    generate_admin_token()
