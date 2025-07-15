from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository
from app import db
from sqlalchemy.exc import SQLAlchemyError

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(db.session, Place)

    def get_places_by_location(self, latitude, longitude, radius=10):
        """Rechercher les lieux dans un rayon donné"""
        # Formule haversine pour calculer la distance
        query = self.session.query(Place).filter(
            db.func.acos(
                db.func.sin(db.func.radians(latitude)) * 
                db.func.sin(db.func.radians(Place.latitude)) + 
                db.func.cos(db.func.radians(latitude)) * 
                db.func.cos(db.func.radians(Place.latitude)) * 
                db.func.cos(db.func.radians(Place.longitude) - db.func.radians(longitude))
            ) * 6371 <= radius
        )
        return query.all()

    def get_places_by_price_range(self, min_price, max_price):
        """Rechercher les lieux dans une fourchette de prix"""
        return self.session.query(Place).filter(
            Place.price.between(min_price, max_price)
        ).all()

    def get_places_by_title(self, title):
        """Rechercher les lieux par titre partiel"""
        return self.session.query(Place).filter(
            Place.title.ilike(f'%{title}%')
        ).all()

    def update_location(self, place_id, latitude, longitude):
        """Mettre à jour la localisation d'un lieu"""
        try:
            place = self.get(place_id)
            if place:
                place.latitude = latitude
                place.longitude = longitude
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            raise
