from app import create_app, db, bcrypt
from app.models.user import User
from config import config

app = create_app(config['development'])

with app.app_context():
    # Créer l'administrateur
    admin = User(
        first_name='Admin',
        last_name='User',
        email='admin@example.com',
        password='adminpass123',
        is_admin=True
    )
    
    db.session.add(admin)
    db.session.commit()
    print('Administrateur créé avec succès !')
