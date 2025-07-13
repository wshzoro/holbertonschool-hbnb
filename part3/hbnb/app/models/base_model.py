from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Update the updated_at timestamp and commit the object."""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data: dict):
        """Update the model with a dict of new values and save."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
