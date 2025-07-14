from app.models.baseclass import BaseModel
from app import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    # Colonnes de base héritées de BaseModel
    # id, created_at, updated_at

    # Colonnes spécifiques à Amenity
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def to_dict(self, include_relationships=False):
        """Convertir l'objet en dictionnaire"""
        result = super().to_dict()
        if include_relationships:
            result['places'] = [place.to_dict() for place in self.places]
        return result