from app.models.baseclass import BaseModel
from app import db
from app.models.association_tables import place_amenity
from app.models.amenity import Amenity

class Place(BaseModel):
    __tablename__ = 'places'

    # Colonnes de base héritées de BaseModel
    # id, created_at, updated_at

    # Colonnes spécifiques à Place
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relations
    owner = db.relationship('User', backref=db.backref('user_places', lazy=True))
    reviews = db.relationship('Review', backref=db.backref('place_reviews', lazy=True))
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        backref=db.backref('place_amenities', lazy=True),
        lazy=True
    )

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

    def to_dict(self, include_relationships=False):
        """Convertir l'objet en dictionnaire"""
        result = super().to_dict()
        if include_relationships:
            result['owner'] = self.owner.to_dict() if self.owner else None
            result['reviews'] = [review.to_dict() for review in self.reviews]
            result['amenities'] = [amenity.to_dict() for amenity in self.amenities]
        return result
