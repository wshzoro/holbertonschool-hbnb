from app.models.baseclass import BaseModel
from app import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    # Colonnes de base héritées de BaseModel
    # id, created_at, updated_at

    # Colonnes spécifiques à Review
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # Relations
    user = db.relationship('User', backref=db.backref('user_reviews', lazy=True, overlaps='reviews'))
    place = db.relationship('Place', backref=db.backref('place_reviews', lazy=True, overlaps='reviews'))

    def __init__(self, text, rating, user_id, place_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    def to_dict(self, include_relationships=False):
        """Convertir l'objet en dictionnaire"""
        result = super().to_dict()
        if include_relationships:
            result['user'] = self.user.to_dict() if self.user else None
            result['place'] = self.place.to_dict() if self.place else None
        return result
