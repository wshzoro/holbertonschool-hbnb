from .baseclass import BaseModel
from .user import User
from .place import Place
from .review import Review
from .amenity import Amenity
from app import db

def init_models():
    """Initialise les modèles SQLAlchemy."""
    # Configuration des relations
    Place.amenities = db.relationship(
        'Amenity',
        secondary='place_amenity',
        lazy='dynamic'
    )
