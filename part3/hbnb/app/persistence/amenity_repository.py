from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository
from app import db
from sqlalchemy.exc import SQLAlchemyError

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        """Rechercher un équipement par nom"""
        return self.model.query.filter(
            Amenity.name.ilike(f'%{name}%')
        ).first()

    def get_amenities_by_place(self, place_id):
        """Rechercher les équipements d'un lieu"""
        return self.model.query.filter(
            Amenity.places.any(id=place_id)
        ).all()

    def get_places_with_amenity(self, amenity_id):
        """Rechercher les lieux avec un équipement"""
        return self.model.query.filter(
            Amenity.places.any(id=amenity_id)
        ).all()

    def update_name(self, amenity_id, new_name):
        """Mettre à jour le nom d'un équipement"""
        if not new_name or not new_name.strip():
            raise ValueError("Le nom ne peut pas être vide")
        
        try:
            amenity = self.get(amenity_id)
            if amenity:
                amenity.name = new_name
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            raise
