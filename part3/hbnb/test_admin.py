from app.models.user import User
from app import db, create_app

def test_admin_role():
    app = create_app()
    with app.app_context():
        # Récupérer l'utilisateur admin
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            print("Erreur: L'admin n'existe pas")
            return
        
        # Vérifier le rôle admin
        if not admin.is_admin:
            print("Erreur: L'admin n'a pas le rôle admin")
            return
        
        print("L'admin a bien le rôle admin")

if __name__ == '__main__':
    test_admin_role()
