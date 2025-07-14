from app import create_app, db

def init_db():
    """Initialize the database by creating all tables."""
    app = create_app("config.DevelopmentConfig")
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
