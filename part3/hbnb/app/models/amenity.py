from app import db
import uuid

from app.models.base_model import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    name = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)