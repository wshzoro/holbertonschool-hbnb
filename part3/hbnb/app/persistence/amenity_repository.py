from app.models.amenity import Amenity
from app import db
from sqlalchemy.orm import Session
from .repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self, session: Session = None):
        if session is None:
            session = db.session
        super().__init__(session, Amenity)

    # Ajoute ici des méthodes spécifiques à Amenity si besoin
