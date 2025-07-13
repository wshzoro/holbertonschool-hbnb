from app import db
import uuid

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        self.name = name