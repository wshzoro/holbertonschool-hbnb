from app.models.place import Place
from app import db
from sqlalchemy.orm import Session
from .repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self, session: Session = None):
        if session is None:
            session = db.session
        super().__init__(session, Place)

    # Ajoute ici des méthodes spécifiques à Place si besoin
