from app import create_app, db
from config import config

app = create_app(config['development'])

with app.app_context():
    db.create_all()
    print('Base de données créée avec succès !')
