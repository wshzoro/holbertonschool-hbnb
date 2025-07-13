from app import db
import uuid
from app.models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36))
    place_id = db.Column(db.String(36))  

    def __init__(self, text, rating, user_id, place_id):
        self.text = text
        self.rating = rating
        self.place_id = place_id
