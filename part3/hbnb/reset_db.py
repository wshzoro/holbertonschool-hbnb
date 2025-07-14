from app import create_app, db
from config import config

app = create_app(config['development'])

with app.app_context():
    db.drop_all()
    db.create_all()
    print('Base de données recréée avec succès !')
