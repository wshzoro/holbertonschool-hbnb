import argparse
from app import create_app, db
from config import config

def init_db(drop=False):
    """
    Initialise la base de données.
    Si 'drop' est True, supprime toutes les tables avant de les recréer.
    """
    app = create_app(config['development'])
    with app.app_context():
        if drop:
            db.drop_all()
            print("Tables supprimées.")
        db.create_all()
        print("Base de données initialisée avec succès.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Initialise la base de données HBnB.")
    parser.add_argument('--drop', action='store_true', help="Supprime toutes les tables avant de recréer")
    args = parser.parse_args()

    init_db(drop=args.drop)
