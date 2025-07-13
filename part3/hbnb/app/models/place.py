from app import db
import uuid

class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    reviews = db.relationship('Review', backref='place', lazy=True)
    # amenities: à faire plus tard (many-to-many)

    def __init__(self, name, description, price, longitude, latitude, owner_id):
        self.name = name
        self.description = description
        self.price = price
        self.longitude = longitude
        self.latitude = latitude
        self.owner_id = owner_id

