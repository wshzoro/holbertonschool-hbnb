from app import db
import uuid

from app.models.base_model import BaseModel
from app import db

class Place(BaseModel):
    __tablename__ = 'places'
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    city = db.Column(db.String(128))
    price = db.Column(db.Float)
    owner_id = db.Column(db.String(36))
