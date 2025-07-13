from app.models.review import Review
from app import db
from sqlalchemy.orm import Session
from .repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self, session: Session = None):
        if session is None:
            session = db.session
        super().__init__(session, Review)

    # Ajoute ici des méthodes spécifiques à Review si besoin
